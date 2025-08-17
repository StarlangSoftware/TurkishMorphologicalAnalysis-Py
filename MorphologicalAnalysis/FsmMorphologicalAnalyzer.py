import copy
import re

import pkg_resources

from Corpus.Sentence import Sentence
from DataStructure.Cache.LRUCache import LRUCache
from Dictionary.Trie.Trie import Trie
from Dictionary.TxtDictionary import TxtDictionary
from Dictionary.TxtWord import TxtWord
from Dictionary.Word import Word
from Util.FileUtils import FileUtils

from MorphologicalAnalysis.FiniteStateMachine import FiniteStateMachine
from MorphologicalAnalysis.FsmParse import FsmParse
from MorphologicalAnalysis.FsmParseList import FsmParseList
from MorphologicalAnalysis.MetamorphicParse import MetamorphicParse
from MorphologicalAnalysis.MorphologicalParse import MorphologicalParse
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag
from MorphologicalAnalysis.State import State
from MorphologicalAnalysis.Transition import Transition


class FsmMorphologicalAnalyzer:
    __dictionary_trie: Trie
    __suffix_trie: Trie
    __finite_state_machine: FiniteStateMachine
    __dictionary: TxtDictionary
    __cache: LRUCache
    __most_used_patterns = {}
    __parsed_surface_forms = None
    __pronunciations = {}

    MAX_DISTANCE = 2

    def __init__(self,
                 dictionaryFileName=None,
                 misspelledFileName=None,
                 fileName=pkg_resources.resource_filename(__name__, 'data/turkish_finite_state_machine.xml'),
                 cacheSize=10000000):
        """
        Constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
        given input dictionary file name and by using turkish_finite_state_machine.xml file.

        PARAMETERS
        ----------
        fileName : str
            the file to read the finite state machine.
        cacheSize : int
            the size of the LRUCache.
        dictionaryFileName : str
            the file to read the dictionary.
        misspelledFileName: str
            the file to read the misspelled file name.
        """
        if dictionaryFileName is None:
            self.__dictionary = TxtDictionary()
        else:
            self.__dictionary = TxtDictionary(dictionaryFileName, misspelledFileName)
        self.__finite_state_machine = FiniteStateMachine(fileName)
        self.__dictionary_trie = self.__dictionary.prepareTrie()
        self.prepareSuffixTrie(pkg_resources.resource_filename(__name__, 'data/suffixes.txt'))
        self.__cache = LRUCache(cacheSize)
        self.addPronunciations(pkg_resources.resource_filename(__name__, 'data/pronunciations.txt'))

    def reverseString(self, s: str) -> str:
        """
        Constructs and returns the reverse string of a given string.
        :param s: String to be reversed.
        :return: Reverse of a given string.
        """
        result = ""
        for i in range(len(s) - 1, -1, -1):
            result += s[i]
        return result

    def prepareSuffixTrie(self, fileName: str):
        """
        Constructs the suffix trie from the input file suffixes.txt. suffixes.txt contains the most frequent 6000
        suffixes that a verb or a noun can take. The suffix trie is a trie that stores these suffixes in reverse form,
        which can be then used to match a given word for its possible suffix content.
        :param fileName: Name of the file that contains the suffixes
        """
        self.__suffix_trie = Trie()
        file = open(fileName, "r")
        lines = file.readlines()
        file.close()
        for suffix in lines:
            reverse_suffix = self.reverseString(suffix.strip())
            self.__suffix_trie.addWord(reverse_suffix, Word(reverse_suffix))

    def addParsedSurfaceForms(self, fileName: str):
        """
        Reads the file for correct surface forms and their most frequent root forms, in other words, the surface forms
        which have at least one morphological analysis in  Turkish.
        :param fileName: Input file containing analyzable surface forms and their root forms.
        """
        self.__parsed_surface_forms = FileUtils.readHashMap(fileName)

    def addPronunciations(self, fileName: str):
        """
        Reads the file for foreign words and their pronunciations.
        :param fileName: Input file containing foreign words and their pronunciations.
        """
        self.__pronunciations = FileUtils.readHashMap(fileName)

    def getPossibleWords(self,
                         morphologicalParse: MorphologicalParse,
                         metamorphicParse: MetamorphicParse) -> set:
        """
        The getPossibleWords method takes MorphologicalParse and MetamorphicParse as input.
        First it determines whether the given morphologicalParse is the root verb and whether it contains a verb tag.
        Then it creates new transition with -mak and creates a new set result.

        It takes the given MetamorphicParse input as currentWord and if there is a compound word starting with the
        currentWord, it gets this compoundWord from dictionaryTrie. If there is a compoundWord and the difference of the
        currentWord and compundWords is less than 3 than compoundWord is added to the result, otherwise currentWord is
        added

        Then it gets the root from parse input as a currentRoot. If it is not null, and morphologicalParse input is
        verb, it directly adds the verb to result after making transition to currentRoot with currentWord String. Else,
        it creates a new transition with -lar and make this transition then adds to the result.

        PARAMETERS
        ----------
        morphologicalParse : MorphologicalParse
            MorphologicalParse type input.
        metamorphicParse : MetamorphicParse
            MetamorphicParse type input.

        RETURNS
        -------
        set
            set result.
        """
        is_root_verb = morphologicalParse.getRootPos() == "VERB"
        contains_verb = morphologicalParse.containsTag(MorphologicalTag.VERB)
        verb_transition = Transition("mAk")
        result = set()
        if metamorphicParse is None or metamorphicParse.getWord() is None:
            return result
        current_word = metamorphicParse.getWord().getName()
        plural_index = -1
        compound_word = self.__dictionary_trie.getCompundWordStartingWith(current_word)
        if not is_root_verb:
            if compound_word is not None and len(compound_word.getName()) - len(current_word) < 3:
                result.add(compound_word.getName())
            result.add(current_word)
        current_root = self.__dictionary.getWord(metamorphicParse.getWord().getName())
        if current_root is None and compound_word is not None:
            current_root = compound_word
        if current_root is not None:
            if is_root_verb:
                verb_word = verb_transition.makeTransitionNoStartState(current_root, current_word)
                result.add(verb_word)
            plural_word = None
            for i in range(1, metamorphicParse.size()):
                transition = Transition(metamorphicParse.getMetaMorpheme(i))
                if metamorphicParse.getMetaMorpheme(i) == "lAr":
                    plural_word = current_word
                    plural_index = i + 1
                current_word = transition.makeTransitionNoStartState(current_root, current_word)
                result.add(current_word)
                if contains_verb:
                    verb_word = verb_transition.makeTransitionNoStartState(current_root, current_word)
                    result.add(verb_word)
            if plural_word is not None:
                current_word = plural_word
                for i in range(plural_index, metamorphicParse.size()):
                    transition = Transition(metamorphicParse.getMetaMorpheme(i))
                    current_word = transition.makeTransitionNoStartState(current_root, current_word)
                    result.add(current_word)
                    if contains_verb:
                        verb_word = verb_transition.makeTransitionNoStartState(current_root, current_word)
                        result.add(verb_word)
        return result

    def getDictionary(self) -> TxtDictionary:
        """
        The getDictionary method is used to get TxtDictionary.

        RETURNS
        -------
        TxtDictionary
            TxtDictionary type dictionary.
        """
        return self.__dictionary

    def getFiniteStateMachine(self) -> FiniteStateMachine:
        """
        The getFiniteStateMachine method is used to get FiniteStateMachine.

        RETURNS
        -------
        FiniteStateMachine
            FiniteStateMachine type finiteStateMachine.
        """
        return self.__finite_state_machine

    def __isPossibleSubstring(self,
                              shortString: str,
                              longString: str,
                              root: TxtWord) -> bool:
        """
        The isPossibleSubstring method first checks whether given short and long strings are equal to root word.
        Then, compares both short and long strings' chars till the last two chars of short string. In the presence of
        mismatch, false is returned. On the other hand, it counts the distance between two strings until it becomes
        greater than 2, which is the MAX_DISTANCE also finds the index of the last char.

        If the substring is a rootWord and equals to 'ben', which is a special case or root holds the
        lastIdropsDuringSuffixation or lastIdropsDuringPassiveSuffixation conditions, then it returns true if distance
        is not greater than MAX_DISTANCE.

        On the other hand, if the shortStrong ends with one of these chars 'e, a, p, ç, t, k' and it 's a rootWord with
        the conditions of rootSoftenDuringSuffixation, vowelEChangesToIDuringYSuffixation,
        vowelAChangesToIDuringYSuffixation or endingKChangesIntoG then it returns true if the last index is not equal to
        2 and distance is not greater than MAX_DISTANCE and false otherwise.

        PARAMETERS
        ----------
        shortString : str
            the possible substring.
        longString : str
            the long string to compare with substring.
        root : TxtWord
            the root of the long string.

        RETURNS
        -------
        bool
            True if given substring is the actual substring of the longString, false otherwise.
        """
        root_word = shortString == root.getName() or longString == root.getName()
        distance = 0
        last = 1
        for j in range(len(shortString)):
            if shortString[j] != longString[j]:
                if j < len(shortString) - 2:
                    return False
                last = len(shortString) - j
                distance = distance + 1
                if distance > self.MAX_DISTANCE:
                    break
        if root_word and (root.getName() == "ben" or root.getName() == "sen" or root.lastIdropsDuringSuffixation()
                         or root.lastIdropsDuringPassiveSuffixation()):
            return distance <= self.MAX_DISTANCE
        elif shortString.endswith("e") or shortString.endswith("a") or shortString.endswith("p") \
                or shortString.endswith("ç") or shortString.endswith("t") or shortString.endswith("k") \
                or (root_word and (root.rootSoftenDuringSuffixation() or root.vowelEChangesToIDuringYSuffixation()
                                  or root.vowelAChangesToIDuringYSuffixation() or root.endingKChangesIntoG())):
            return last != 2 and distance <= self.MAX_DISTANCE - 1
        else:
            return distance <= self.MAX_DISTANCE - 2

    def __initializeParseList(self,
                              fsmParse: list,
                              root: TxtWord,
                              isProper: bool):
        """
        The initializeParseList method initializes the given given fsm ArrayList with given root words by parsing them.

        It checks many conditions;
        isPlural; if root holds the condition then it gets the state with the name of NominalRootPlural, then
        creates a new parsing and adds this to the input fsmParse Arraylist.
        Ex : Açıktohumlular

        !isPlural and isPortmanteauEndingWithSI, if root holds the conditions then it gets the state with the
        name of NominalRootNoPossesive.
        Ex : Balarısı

        !isPlural and isPortmanteau, if root holds the conditions then it gets the state with the name of
        CompoundNounRoot.
        Ex : Aslanağızı

        !isPlural, !isPortmanteau and isHeader, if root holds the conditions then it gets the state with the
        name of HeaderRoot.
        Ex :  </title>

        !isPlural, !isPortmanteau and isInterjection, if root holds the conditions then it gets the state
        with the name of InterjectionRoot.
        Ex : Hey, Aa

        !isPlural, !isPortmanteau and isDuplicate, if root holds the conditions then it gets the state
        with the name of DuplicateRoot.

        !isPlural, !isPortmanteau and isCode, if root holds the conditions then it gets the state
        with the name of CodeRoot.
        Ex : 9400f,

        !isPlural, !isPortmanteau and isMetric, if root holds the conditions then it gets the state
        with the name of MetricRoot.
        Ex : 11x8x12,

        !isPlural, !isPortmanteau and isNumeral, if root holds the conditions then it gets the state
        with the name of CardinalRoot.

        !isPlural, !isPortmanteau and isReal, if root holds the conditions then it gets the state
        with the name of RealRoot.

        !isPlural, !isPortmanteau and isFraction, if root holds the conditions then it gets the state
        with the name of FractionRoot.
        Ex : 1/2

        !isPlural, !isPortmanteau and isDate, if root holds the conditions then it gets the state
        with the name of DateRoot.
        Ex : 11/06/2018

        !isPlural, !isPortmanteau and isPercent, if root holds the conditions then it gets the state
        with the name of PercentRoot.
        Ex : %12.5

        !isPlural, !isPortmanteau and isRange, if root holds the conditions then it gets the state
        with the name of RangeRoot.
        Ex : 3-5

        !isPlural, !isPortmanteau and isTime, if root holds the conditions then it gets the state
        with the name of TimeRoot.
        Ex : 13:16:08

        !isPlural, !isPortmanteau and isOrdinal, if root holds the conditions then it gets the state
        with the name of OrdinalRoot.
        Ex : Altıncı

        !isPlural, !isPortmanteau, and isVerb if root holds the conditions then it gets the state
        with the name of VerbalRoot. Or isPassive, then it gets the state with the name of PassiveHn.
        Ex : Anla (!isPAssive)
        Ex : Çağrıl (isPassive)

        !isPlural, !isPortmanteau and isPronoun, if root holds the conditions then it gets the state
        with the name of PronounRoot. There are 6 different Pronoun state names, REFLEX, QUANT, QUANTPLURAL, DEMONS,
        PERS, QUES.
        REFLEX = Reflexive Pronouns Ex : kendi
        QUANT = Quantitative Pronouns Ex : öbür, hep, kimse, hiçbiri, bazı, kimi, biri
        QUANTPLURAL = Quantitative Plural Pronouns Ex : tümü, çoğu, hepsi
        DEMONS = Demonstrative Pronouns Ex : o, bu, şu
        PERS = Personal Pronouns Ex : ben, sen, o, biz, siz, onlar
        QUES = Interrogatıve Pronouns Ex : nere, ne, kim, hangi

        !isPlural, !isPortmanteau and isAdjective, if root holds the conditions then it gets the state
        with the name of AdjectiveRoot.
        Ex : Absürt, Abes

        !isPlural, !isPortmanteau and isPureAdjective, if root holds the conditions then it gets the state
        with the name of Adjective.
        Ex : Geçmiş, Cam

        !isPlural, !isPortmanteau and isNominal, if root holds the conditions then it gets the state
        with the name of NominalRoot.
        Ex : Görüş

        !isPlural, !isPortmanteau and isProper, if root holds the conditions then it gets the state
        with the name of ProperRoot.
        Ex : Abdi

        !isPlural, !isPortmanteau and isQuestion, if root holds the conditions then it gets the state
        with the name of QuestionRoot.
        Ex : Mi, mü

        !isPlural, !isPortmanteau and isDeterminer, if root holds the conditions then it gets the state
        with the name of DeterminerRoot.
        Ex : Çok, bir

        !isPlural, !isPortmanteau and isConjunction, if root holds the conditions then it gets the state
        with the name of ConjunctionRoot.
        Ex : Ama , ancak

        !isPlural, !isPortmanteau and isPostP, if root holds the conditions then it gets the state
        with the name of PostP.
        Ex : Ait, dair

        !isPlural, !isPortmanteau and isAdverb, if root holds the conditions then it gets the state
        with the name of AdverbRoot.
        Ex : Acilen

        PARAMETERS
        ----------
        fsmParse : list
            list to initialize.
        root : TxtWord
            word to check properties and add to fsmParse according to them.
        isProper : bool
            is used to check a word is proper or not.
        """
        if root.isPlural():
            current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("NominalRootPlural"))
            fsmParse.append(current_fsm_parse)
        elif root.isPortmanteauEndingWithSI():
            current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 2],
                                       self.__finite_state_machine.getState("CompoundNounRoot"))
            fsmParse.append(current_fsm_parse)
            current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("NominalRootNoPossesive"))
            fsmParse.append(current_fsm_parse)
        elif root.isPortmanteau():
            if root.isPortmanteauFacedVowelEllipsis():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("NominalRootNoPossesive"))
                fsmParse.append(current_fsm_parse)
                current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 2] +
                                           root.getName()[len(root.getName()) - 1] +
                                           root.getName()[len(root.getName()) - 2],
                                           self.__finite_state_machine.getState("CompoundNounRoot"))
            elif root.isPortmanteauFacedSoftening():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("NominalRootNoPossesive"))
                fsmParse.append(current_fsm_parse)
                if root.getName()[len(root.getName()) - 2] == "b":
                    current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 2] + "p",
                                               self.__finite_state_machine.getState("CompoundNounRoot"))
                elif root.getName()[len(root.getName()) - 2] == "c":
                    current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 2] + "ç",
                                               self.__finite_state_machine.getState("CompoundNounRoot"))
                elif root.getName()[len(root.getName()) - 2] == "d":
                    current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 2] + "t",
                                               self.__finite_state_machine.getState("CompoundNounRoot"))
                elif root.getName()[len(root.getName()) - 2] == "ğ":
                    current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 2] + "k",
                                               self.__finite_state_machine.getState("CompoundNounRoot"))
                else:
                    current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 1],
                                               self.__finite_state_machine.getState("CompoundNounRoot"))
            else:
                current_fsm_parse = FsmParse(root.getName()[:len(root.getName()) - 1],
                                           self.__finite_state_machine.getState("CompoundNounRoot"))
            fsmParse.append(current_fsm_parse)
        else:
            if root.isHeader():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("HeaderRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isInterjection():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("InterjectionRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isDuplicate():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("DuplicateRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isCode():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("CodeRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isMetric():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("MetricRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isNumeral():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("CardinalRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isReal():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("RealRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isFraction():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("FractionRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isDate():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("DateRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isPercent():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PercentRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isRange():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("RangeRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isTime():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("TimeRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isOrdinal():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("OrdinalRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isVerb() or root.isPassive():
                if root.verbType() != "":
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("VerbalRoot("
                                                                                          + root.verbType() + ")"))
                elif not root.isPassive():
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("VerbalRoot"))
                else:
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PassiveHn"))
                fsmParse.append(current_fsm_parse)
            if root.isPronoun():
                if root.getName() == "kendi":
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PronounRoot(REFLEX)"))
                    fsmParse.append(current_fsm_parse)
                if root.getName() == "öbür" or root.getName() == "öteki" or root.getName() == "hep" or \
                        root.getName() == "kimse" or root.getName() == "diğeri" or root.getName() == "hiçbiri" or \
                        root.getName() == "böylesi" or root.getName() == "birbiri" or root.getName() == "birbirleri" or \
                        root.getName() == "biri" or root.getName() == "başkası" or root.getName() == "bazı" or \
                        root.getName() == "kimi":
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PronounRoot(QUANT)"))
                    fsmParse.append(current_fsm_parse)
                if root.getName() == "tümü" or root.getName() == "topu" or root.getName() == "herkes" or \
                        root.getName() == "cümlesi" or root.getName() == "çoğu" or root.getName() == "birçoğu" or \
                        root.getName() == "birkaçı" or root.getName() == "birçokları" or root.getName() == "hepsi":
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PronounRoot(QUANTPLURAL)"))
                    fsmParse.append(current_fsm_parse)
                if root.getName() == "o" or root.getName() == "bu" or root.getName() == "şu":
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PronounRoot(DEMONS)"))
                    fsmParse.append(current_fsm_parse)
                if root.getName() == "ben" or root.getName() == "sen" or root.getName() == "o" or \
                        root.getName() == "biz" or root.getName() == "siz" or root.getName() == "onlar":
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PronounRoot(PERS)"))
                    fsmParse.append(current_fsm_parse)
                if root.getName() == "nere" or root.getName() == "ne" or root.getName() == "kaçı" or \
                        root.getName() == "kim" or root.getName() == "hangi":
                    current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PronounRoot(QUES)"))
                    fsmParse.append(current_fsm_parse)
            if root.isAdjective():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("AdjectiveRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isPureAdjective():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("Adjective"))
                fsmParse.append(current_fsm_parse)
            if root.isNominal():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("NominalRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isAbbreviation():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("NominalRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isProperNoun() and isProper:
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("ProperRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isQuestion():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("QuestionRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isDeterminer():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("DeterminerRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isConjunction():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("ConjunctionRoot"))
                fsmParse.append(current_fsm_parse)
            if root.isPostP():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("PostP"))
                fsmParse.append(current_fsm_parse)
            if root.isAdverb():
                current_fsm_parse = FsmParse(root, self.__finite_state_machine.getState("AdverbRoot"))
                fsmParse.append(current_fsm_parse)

    def __initializeParseListFromRoot(self,
                                      parseList: list,
                                      root: TxtWord,
                                      isProper: bool):
        """
        The initializeParseListFromRoot method is used to create a list which consists of initial fsm parsings. First,
        traverses this HashSet and uses each word as a root and calls initializeParseList method with this root and
        list.

        PARAMETERS
        ----------
        parseList : list
            list to initialize.
        root : TxtWord
            the root form to generate initial parse list.
        isProper : bool
            is used to check a word is proper or not.
        """
        self.__initializeParseList(parseList, root, isProper)
        if root.obeysAndNotObeysVowelHarmonyDuringAgglutination():
            new_root = copy.deepcopy(root)
            new_root.removeFlag("IS_UU")
            new_root.removeFlag("IS_UUU")
            self.__initializeParseList(parseList, new_root, isProper)
        if root.rootSoftenAndNotSoftenDuringSuffixation():
            new_root = copy.deepcopy(root)
            new_root.removeFlag("IS_SD")
            new_root.removeFlag("IS_SDD")
            self.__initializeParseList(parseList, new_root, isProper)
        if root.lastIDropsAndNotDropDuringSuffixation():
            new_root = copy.deepcopy(root)
            new_root.removeFlag("IS_UD")
            new_root.removeFlag("IS_UDD")
            self.__initializeParseList(parseList, new_root, isProper)
        if root.duplicatesAndNotDuplicatesDuringSuffixation():
            new_root = copy.deepcopy(root)
            new_root.removeFlag("IS_ST")
            new_root.removeFlag("IS_STT")
            self.__initializeParseList(parseList, new_root, isProper)
        if root.endingKChangesIntoG() and root.containsFlag("IS_OA"):
            new_root = copy.deepcopy(root)
            new_root.removeFlag("IS_OA")
            self.__initializeParseList(parseList, new_root, isProper)

    def __initializeParseListFromSurfaceForm(self,
                                             surfaceForm: str,
                                             isProper: bool) -> list:
        """
        The initializeParseListFromSurfaceForm method is used to create a list which consists of initial fsm parsings.
        First, it calls getWordsWithPrefix methods by using input String surfaceForm and generates a set. Then,
        traverses this set and uses each word as a root and calls initializeParseListFromRoot method with this root and
        list.

        PARAMETERS
        ----------
        surfaceForm : str
            the String used to generate a HashSet of words.
        isProper : bool
            is used to check a word is proper or not.

        RETURNS
        -------
        list
            initialFsmParse list.
        """
        initial_fsm_parse = []
        if len(surfaceForm) == 0:
            return initial_fsm_parse
        words = self.__dictionary_trie.getWordsWithPrefix(surfaceForm)
        for word in words:
            self.__initializeParseListFromRoot(initial_fsm_parse, word, isProper)
        return initial_fsm_parse

    def __addNewParsesFromCurrentParse(self,
                                       currentFsmParse: FsmParse,
                                       fsmParse: list,
                                       maxLengthOrSurfaceForm,
                                       root: TxtWord):
        """
        The addNewParsesFromCurrentParseSurfaceForm method initially gets the final suffixes from input currentFsmParse
        called as currentState, and by using the currentState information it gets the currentSurfaceForm. Then loops
        through each currentState's transition. If the currentTransition is possible, it makes the transition.
        The addNewParsesFromCurrentParseMaxLength method initially gets the final suffixes from input currentFsmParse
        called as currentState, and by using the currentState information it gets the new analysis. Then loops through
        each currentState's transition. If the currentTransition is possible, it makes the transition.

        PARAMETERS
        ----------
        currentFsmParse : FsmParse
            FsmParse type input.
        fsmParse : list
            List of FsmParse.
        maxLengthOrSurfaceForm
            Maximum length of the parse.
        root : TxtWord
            TxtWord used to make transition.
        """
        current_state = currentFsmParse.getFinalSuffix()
        current_surface_form = currentFsmParse.getSurfaceForm()
        if isinstance(maxLengthOrSurfaceForm, int):
            max_length = maxLengthOrSurfaceForm
            for current_transition in self.__finite_state_machine.getTransitions(current_state):
                if current_transition.transitionPossibleForParse(currentFsmParse) \
                        and (current_surface_form != root.getName()
                             or (current_surface_form == root.getName() and
                                 current_transition.transitionPossibleForWord(root, current_state))):
                    tmp = current_transition.makeTransition(root, current_surface_form, currentFsmParse.getStartState())
                    if len(tmp) <= max_length:
                        new_fsm_parse = copy.deepcopy(currentFsmParse)
                        new_fsm_parse.addSuffix(current_transition.toState(), tmp, current_transition.withName(),
                                              current_transition.__str__(), current_transition.toPos())
                        new_fsm_parse.setAgreement(current_transition.withName())
                        fsmParse.append(new_fsm_parse)
        elif isinstance(maxLengthOrSurfaceForm, str):
            surface_form = maxLengthOrSurfaceForm
            for current_transition in self.__finite_state_machine.getTransitions(current_state):
                if current_transition.transitionPossibleForString(currentFsmParse.getSurfaceForm(), surface_form) and \
                        current_transition.transitionPossibleForParse(currentFsmParse) and (
                        current_surface_form != root.getName()
                        or (current_surface_form == root.getName() and
                            current_transition.transitionPossibleForWord(root, current_state))):
                    tmp = current_transition.makeTransition(root, current_surface_form, currentFsmParse.getStartState())
                    if (len(tmp) < len(surface_form) and self.__isPossibleSubstring(tmp, surface_form, root)) or \
                            (len(tmp) == len(surface_form) and (
                                    root.lastIdropsDuringSuffixation() or tmp == surface_form)):
                        new_fsm_parse = copy.deepcopy(currentFsmParse)
                        new_fsm_parse.addSuffix(current_transition.toState(), tmp, current_transition.withName(),
                                              current_transition.__str__(), current_transition.toPos())
                        new_fsm_parse.setAgreement(current_transition.withName())
                        fsmParse.append(new_fsm_parse)

    def __parseExists(self,
                      fsmParse: list,
                      surfaceForm: str) -> bool:
        """
        The parseExists method is used to check the existence of the parse.

        PARAMETERS
        ----------
        fsmParse : list
            List of FsmParse
        surfaceForm : str
            String to use during transition.

        RETURNS
        -------
        bool
            True when the currentState is end state and input surfaceForm id equal to currentSurfaceForm, otherwise false.
        """
        while len(fsmParse) > 0:
            current_fsm_parse = fsmParse.pop(0)
            root = current_fsm_parse.getWord()
            current_state = current_fsm_parse.getFinalSuffix()
            current_surface_form = current_fsm_parse.getSurfaceForm()
            if current_state.isEndState() and current_surface_form == surfaceForm:
                return True
            self.__addNewParsesFromCurrentParse(current_fsm_parse, fsmParse, surfaceForm, root)
        return False

    def __parseWord(self,
                    fsmParse: list,
                    maxLengthOrSurfaceForm) -> list:
        """
        The parseWordSurfaceForm method is used to parse a given fsmParse. It simply adds new parses to the current
        parse by using addNewParsesFromCurrentParse method.
        The parseWordMaxLength method is used to parse a given fsmParse. It simply adds new parses to the current parse
        by using addNewParsesFromCurrentParse method.

        PARAMETERS
        ----------
        fsmParse : list
            a list of FsmParse
        maxLengthOrSurfaceForm
            maximum length of the surfaceform.

        RETURNS
        -------
        list
            Result list which has the currentFsmParse.
        """
        result = []
        result_transition_list = []
        if isinstance(maxLengthOrSurfaceForm, int):
            max_length = maxLengthOrSurfaceForm
            while len(fsmParse) > 0:
                current_fsm_parse = fsmParse.pop(0)
                root = current_fsm_parse.getWord()
                current_state = current_fsm_parse.getFinalSuffix()
                current_surface_form = current_fsm_parse.getSurfaceForm()
                if current_state.isEndState() and len(current_surface_form) <= max_length:
                    current_transition_list = current_surface_form + " " + current_fsm_parse.transitionList()
                    if current_transition_list not in result_transition_list:
                        result.append(current_fsm_parse)
                        current_fsm_parse.constructInflectionalGroups()
                        result_transition_list.append(current_transition_list)
                self.__addNewParsesFromCurrentParse(current_fsm_parse, fsmParse, max_length, root)
        elif isinstance(maxLengthOrSurfaceForm, str):
            surface_form = maxLengthOrSurfaceForm
            while len(fsmParse) > 0:
                current_fsm_parse = fsmParse.pop(0)
                root = current_fsm_parse.getWord()
                current_state = current_fsm_parse.getFinalSuffix()
                current_surface_form = current_fsm_parse.getSurfaceForm()
                if current_state.isEndState() and current_surface_form == surface_form:
                    current_transition_list = current_fsm_parse.transitionList()
                    if current_transition_list not in result_transition_list:
                        result.append(current_fsm_parse)
                        current_fsm_parse.constructInflectionalGroups()
                        result_transition_list.append(current_transition_list)
                self.__addNewParsesFromCurrentParse(current_fsm_parse, fsmParse, surface_form, root)
        return result

    def morphologicalAnalysisRoot(self,
                                  surfaceForm: str,
                                  root: TxtWord,
                                  state=None) -> list:
        """
        The morphologicalAnalysis with 3 inputs is used to initialize an {@link ArrayList} and add a new FsmParse
        with given root and state.

        PARAMETERS
        ----------
        root : TxtWord
            TxtWord input.
        surfaceForm : str
            String input to use for parsing.
        state : str
            String input.

        RETURNS
        -------
        list
            parseWord method with newly populated FsmParse ArrayList and input surfaceForm.
        """
        if state is None:
            initial_fsm_parse = []
            self.__initializeParseListFromRoot(initial_fsm_parse, root, self.isProperNoun(surfaceForm))
        else:
            initial_fsm_parse = [FsmParse(root, self.__finite_state_machine.getState(state))]
        return self.__parseWord(initial_fsm_parse, surfaceForm)

    def generateAllParses(self,
                          root: TxtWord,
                          maxLength: int) -> list:
        """
        The generateAllParses with 2 inputs is used to generate all parses with given root. Then it calls
        initializeParseListFromRoot method to initialize list with newly created ArrayList, input root, and maximum
        length.

        PARAMETERS
        ----------
        root : TxtWord
            TxtWord input.
        maxLength : int
            Maximum length of the surface form.

        RETURNS
        -------
        list
            parseWordMaxLength method with newly populated FsmParse ArrayList and maximum length.
        """
        initial_fsm_parse = []
        if root.isProperNoun():
            self.__initializeParseListFromRoot(initial_fsm_parse, root, True)
        self.__initializeParseListFromRoot(initial_fsm_parse, root, False)
        return self.__parseWord(initial_fsm_parse, maxLength)

    def replaceRootWord(self,
                        parse: FsmParse,
                        newRoot: TxtWord) -> str:
        """
        Replace root word of the current parse with the new root word and returns the new word.

        PARAMETERS
        ----------
        newRoot : TxtWord
            Replaced root word

        RETURNS
        -------
        str
            Root word of the parse will be replaced with the newRoot and the resulting surface form is returned.
        """
        result = newRoot.getName()
        for a_with in parse.getWithList():
            transition = Transition(a_with)
            result = transition.makeTransitionNoStartState(newRoot, result)
        return result

    def replaceWord(self,
                    original: Sentence,
                    previousWord: str,
                    newWord: str) -> Sentence:
        """
        Replaces previous lemma in the sentence with the new lemma. Both lemma can contain multiple words.
        :param original: Original sentence to be replaced with.
        :param previousWord: Root word in the original sentence
        :param newWord: New word to be replaced.
        :return: Newly generated sentence by replacing the previous word in the original sentence with the new word.
        """
        result = Sentence()
        previous_word_multiple = " " in previousWord
        new_word_multiple = " " in newWord
        if previous_word_multiple:
            previous_word_splitted = previousWord.split(" ")
            last_word = previous_word_splitted[len(previous_word_splitted) - 1]
        else:
            last_word = previousWord
        if new_word_multiple:
            new_word_splitted = newWord.split(" ")
            new_root_word = new_word_splitted[len(new_word_splitted) - 1]
        else:
            new_root_word = newWord
        new_root_txt_word = self.__dictionary.getWord(new_root_word)
        parse_list = self.morphologicalAnalysis(original)
        i = 0
        while i < len(parse_list):
            replaced = False
            replaced_word = None
            for j in range(parse_list[i].size()):
                if parse_list[i].getFsmParse(j).root.getName() == last_word and new_root_txt_word is not None:
                    replaced = True
                    replaced_word = self.replaceRootWord(parse_list[i].getFsmParse(j), new_root_txt_word)
            if replaced and replaced_word is not None:
                if previous_word_multiple:
                    for k in range(i - len(previous_word_splitted) + 1):
                        result.addWord(original.getWord(k))
                if new_word_multiple:
                    for k in range(len(new_word_splitted) - 1):
                        if result.wordCount() == 0:
                            result.addWord(Word((new_word_splitted[k][0] + "").upper() + new_word_splitted[k][1:]))
                        else:
                            result.addWord(Word(new_word_splitted[k]))
                if result.wordCount() == 0:
                    replaced_word = (replaced_word[0]).upper() + replaced_word[1:]
                result.addWord(Word(replaced_word))
                if previous_word_multiple:
                    i = i + 1
                    break
            else:
                if not previous_word_multiple:
                    result.addWord(original.getWord(i))
            i = i + 1
        if previous_word_multiple:
            while i < len(parse_list):
                result.addWord(original.getWord(i))
                i = i + 1
        return result

    def __analysisExists(self,
                         rootWord: TxtWord,
                         surfaceForm: str,
                         isProper: bool) -> bool:
        """
        The analysisExists method checks several cases. If the given surfaceForm is a punctuation or double then it
        returns true. If it is not a root word, then it initializes the parse list and returns the parseExists method with
        this newly initialized list and surfaceForm.

        PARAMETERS
        ----------
        rootWord : TxtWord
            TxtWord root.
        surfaceForm : str
            String input.
        isProper : bool
            boolean variable indicates a word is proper or not.

        RETURNS
        -------
        bool
            True if surfaceForm is punctuation or double, otherwise returns parseExist method with given surfaceForm.
        """
        if Word.isPunctuationSymbol(surfaceForm):
            return True
        if self.__isDouble(surfaceForm):
            return True
        if rootWord is not None:
            initial_fsm_parse = []
            self.__initializeParseListFromRoot(initial_fsm_parse, rootWord, isProper)
        else:
            initial_fsm_parse = self.__initializeParseListFromSurfaceForm(surfaceForm, isProper)
        return self.__parseExists(initial_fsm_parse, surfaceForm)

    def __analysis(self,
                   surfaceForm: str,
                   isProper: bool) -> list:
        """
        The analysis method is used by the morphologicalAnalysis method. It gets String surfaceForm as an input and
        checks its type such as punctuation, number or compares with the regex for date, fraction, percent, time, range,
        hashtag, and mail or checks its variable type as integer or double. After finding the right case for given
        surfaceForm, it calls constructInflectionalGroups method which creates sub-word units.

        PARAMETERS
        ----------
        surfaceForm : str
            String to analyse.
        isProper : bool
            is used to indicate the proper words.

        RETURNS
        -------
        list
            List type initialFsmParse which holds the analyses.
        """
        if Word.isPunctuationSymbol(surfaceForm) and surfaceForm != "%":
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("Punctuation", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.__isNumber(surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("CardinalRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.patternMatches("\\d+/\\d+", surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("FractionRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            fsm_parse = FsmParse(surfaceForm, State("DateRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.__isDate(surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("DateRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.patternMatches("\\d+\\\\/\\d+", surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("FractionRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if surfaceForm == "%" or self.__isPercent(surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("PercentRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.__isTime(surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("TimeRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.__isRange(surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("RangeRoot", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if surfaceForm.startswith("#"):
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("Hashtag", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if "@" in surfaceForm:
            initial_fsm_parse = []
            fsm_parse = FsmParse(surfaceForm, State("Email", True, True))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if surfaceForm.endswith(".") and self.__isInteger(surfaceForm[:len(surfaceForm) - 1]):
            initial_fsm_parse = []
            fsm_parse = FsmParse(int(surfaceForm[:len(surfaceForm) - 1]),
                                self.__finite_state_machine.getState("OrdinalRoot"))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.__isInteger(surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(int(surfaceForm), self.__finite_state_machine.getState("CardinalRoot"))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        if self.__isDouble(surfaceForm):
            initial_fsm_parse = []
            fsm_parse = FsmParse(float(surfaceForm), self.__finite_state_machine.getState("RealRoot"))
            fsm_parse.constructInflectionalGroups()
            initial_fsm_parse.append(fsm_parse)
            return initial_fsm_parse
        initial_fsm_parse = self.__initializeParseListFromSurfaceForm(surfaceForm, isProper)
        return self.__parseWord(initial_fsm_parse, surfaceForm)

    def patternMatches(self,
                       expr: str,
                       value: str) -> bool:
        """
        This method uses cache idea to speed up pattern matching in Fsm. __most_used_patterns stores the compiled forms
        of the previously used patterns. When Fsm tries to match a string to a pattern, first we check if it exists in
        __most_used_patterns. If it exists, we directly use the compiled pattern to match the string. Otherwise, new
        pattern is compiled and put in the __most_used_patterns.
        :param expr:
        :param value:
        :return:
        """
        if expr in self.__most_used_patterns:
            return self.__most_used_patterns[expr].fullmatch(value) is not None
        else:
            compiled_expression = re.compile(expr)
            self.__most_used_patterns[expr] = compiled_expression
            return compiled_expression.fullmatch(value) is not None

    def isProperNoun(self, surfaceForm: str) -> bool:
        """
        The isProperNoun method takes surfaceForm String as input and checks its each char whether they are in the range
        of letters between A to Z or one of the Turkish letters such as İ, Ü, Ğ, Ş, Ç, and Ö.

        PARAMETERS
        ----------
        surfaceForm : str
            String to check for proper noun.

        RETURNS
        -------
        bool
            False if surfaceForm is null or length of 0, return true if it is a letter.
        """
        if surfaceForm is None or len(surfaceForm) == 0:
            return False
        return "A" <= surfaceForm[0] <= "Z" or surfaceForm[0] == "Ç" or surfaceForm[0] == "Ö" or surfaceForm[0] == "Ğ" \
               or surfaceForm[0] == "Ü" or surfaceForm[0] == "Ş" or surfaceForm[0] == "İ"

    def __isCode(self, surfaceForm: str) -> bool:
        """
        The isCode method takes surfaceForm String as input and checks if it consists of both letters and numbers
        :param surfaceForm: String to check for code-like word.
        :return: True if it is a code-like word, return false otherwise.
        """
        if surfaceForm is None or len(surfaceForm) == 0:
            return False
        return self.patternMatches(".*[0-9].*", surfaceForm) and \
               self.patternMatches(".*[a-zA-ZçöğüşıÇÖĞÜŞİ].*", surfaceForm)

    def __isPercent(self, surfaceForm: str) -> bool:
        """
        Checks if a given surface form matches to a percent value. It should be something like %4, %45, %4.3 or %56.786
        :param surfaceForm: Surface form to be checked.
        :return: True if the surface form is in percent form
        """
        return self.patternMatches("%(\\d\\d|\\d)", surfaceForm) or \
               self.patternMatches("%(\\d\\d|\\d)\\.\\d+", surfaceForm)

    def __isTime(self, surfaceForm: str) -> bool:
        """
        Checks if a given surface form matches to a time form. It should be something like 3:34, 12:56 etc.
        :param surfaceForm: Surface form to be checked.
        :return: True if the surface form is in time form
        """
        return self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d):(\\d\\d|\\d)", surfaceForm) or \
                self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d)", surfaceForm)

    def __isRange(self, surfaceForm: str) -> bool:
        """
        Checks if a given surface form matches to a range form. It should be something like 123-1400 or 12:34-15:78 or
        3.45-4.67.
        :param surfaceForm: Surface form to be checked.
        :return: True if the surface form is in range form
        """
        return self.patternMatches("\\d+-\\d+", surfaceForm) or \
                            self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d)-(\\d\\d|\\d):(\\d\\d|\\d)", surfaceForm) or \
                            self.patternMatches("(\\d\\d|\\d)\\.(\\d\\d|\\d)-(\\d\\d|\\d)\\.(\\d\\d|\\d)",
                                                surfaceForm)

    def __isDate(self, surfaceForm: str) -> bool:
        """
        Checks if a given surface form matches to a date form. It should be something like 3/10/2023 or 2.3.2012
        :param surfaceForm: Surface form to be checked.
        :return: True if the surface form is in date form
        """
        return self.patternMatches("(\\d\\d|\\d)/(\\d\\d|\\d)/\\d+", surfaceForm) or \
               self.patternMatches("(\\d\\d|\\d)\\.(\\d\\d|\\d)\\.\\d+", surfaceForm)

    def morphologicalAnalysis(self, sentenceOrSurfaceForm):
        """
        The morphologicalAnalysis method is used to analyse a FsmParseList by comparing with the regex.
        It creates a list fsmParse to hold the result of the analysis method. For each surfaceForm input,
        it gets a substring and considers it as a possibleRoot. Then compares with the regex.

        If the surfaceForm input string matches with Turkish chars like Ç, Ş, İ, Ü, Ö, it adds the surfaceForm to Trie
        with IS_OA tag.
        If the possibleRoot contains /, then it is added to the Trie with IS_KESIR tag.
        If the possibleRoot contains \\d\\d|\\d)/(\\d\\d|\\d)/\\d+, then it is added to the Trie with IS_DATE tag.
        If the possibleRoot contains \\d\\d|\\d, then it is added to the Trie with IS_PERCENT tag.
        If the possibleRoot contains \\d\\d|\\d):(\\d\\d|\\d):(\\d\\d|\\d), then it is added to the Trie with IS_ZAMAN
        tag.
        If the possibleRoot contains \\d+-\\d+, then it is added to the Trie with IS_RANGE tag.
        If the possibleRoot is an Integer, then it is added to the Trie with IS_SAYI tag.
        If the possibleRoot is a Double, then it is added to the Trie with IS_REELSAYI tag.

        PARAMETERS
        ----------
        sentenceOrSurfaceForm : str
            String or Sentence to analyse.

        RETURNS
        -------
        list
            list which folds the analysis
        FsmParseList
            fsmParseList which holds the analysis.
        """
        if isinstance(sentenceOrSurfaceForm, Sentence):
            sentence = sentenceOrSurfaceForm
            result = []
            for i in range(sentence.wordCount()):
                original_form = sentence.getWord(i).getName()
                spell_corrected_form = self.__dictionary.getCorrectForm(original_form)
                if len(spell_corrected_form) == 0:
                    spell_corrected_form = original_form
                word_fsm_parse_list = self.morphologicalAnalysis(spell_corrected_form)
                result.append(word_fsm_parse_list)
            return result
        elif isinstance(sentenceOrSurfaceForm, str):
            possible_root_lowercased = ""
            lowercased = self.__toLower(sentenceOrSurfaceForm)
            is_root_replaced = False
            surface_form = sentenceOrSurfaceForm
            if self.__parsed_surface_forms is not None and surface_form in self.__parsed_surface_forms \
                    and not self.__isRange(surface_form) and not self.__isTime(surface_form) \
                    and not self.__isInteger(surface_form) and not self.__isDouble(surface_form) \
                    and not self.__isDate(surface_form) and not self.__isPercent(surface_form):
                return FsmParseList([FsmParse(Word(surface_form))])
            if self.__cache.contains(surface_form):
                return self.__cache.get(surface_form)
            if self.patternMatches("(\\w|Ç|Ş|İ|Ü|Ö)\\.", surface_form):
                self.__dictionary_trie.addWord(lowercased, TxtWord(lowercased, "IS_OA"))
            default_fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
            if len(default_fsm_parse) > 0:
                fsm_parse_list = FsmParseList(default_fsm_parse)
                self.__cache.add(surface_form, fsm_parse_list)
                return fsm_parse_list
            fsm_parse = []
            if "'" in surface_form:
                possible_root = surface_form[:surface_form.index('\'')]
                if len(possible_root) > 0:
                    if "/" in possible_root or "\\/" in possible_root:
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_KESIR"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif self.__isDate(possible_root):
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_DATE"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif self.patternMatches("\\d+/\\d+", possible_root):
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_KESIR"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif self.__isPercent(possible_root):
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_PERCENT"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif self.__isTime(possible_root):
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_ZAMAN"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif self.__isRange(possible_root):
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_RANGE"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif self.__isInteger(possible_root):
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_SAYI"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif self.__isDouble(possible_root):
                        self.__dictionary_trie.addWord(possible_root, TxtWord(possible_root, "IS_REELSAYI"))
                        fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
                    elif Word.isCapital(possible_root) or possible_root[0:1] in "QXW":
                        possible_root_lowercased = self.__toLower(possible_root)
                        if possible_root_lowercased in self.__pronunciations:
                            is_root_replaced = True
                            pronunciation = self.__pronunciations[possible_root_lowercased]
                            word = self.__dictionary.getWord(pronunciation)
                            if word is not None and isinstance(word, TxtWord):
                                word.addFlag("IS_OA")
                            else:
                                new_word = TxtWord(pronunciation, "IS_OA")
                                self.__dictionary_trie.addWord(pronunciation, new_word)
                            replaced_word = pronunciation + lowercased[len(possible_root_lowercased):]
                            fsm_parse = self.__analysis(replaced_word, self.isProperNoun(surface_form))
                        else:
                            word = self.__dictionary.getWord(possible_root_lowercased)
                            if word is not None and isinstance(word, TxtWord):
                                word.addFlag("IS_OA")
                            else:
                                new_word = TxtWord(possible_root_lowercased, "IS_OA")
                                self.__dictionary_trie.addWord(possible_root_lowercased, new_word)
                            fsm_parse = self.__analysis(lowercased, self.isProperNoun(surface_form))
            if is_root_replaced:
                for parse in fsm_parse:
                    parse.restoreOriginalForm(possible_root_lowercased, pronunciation)
            fsm_parse_list = FsmParseList(fsm_parse)
            if fsm_parse_list.size() > 0:
                self.__cache.add(surface_form, fsm_parse_list)
            return fsm_parse_list

    def rootOfPossiblyNewWord(self, surfaceForm: str) -> [TxtWord]:
        """
        Identifies a possible new root word for a given surface form. It also adds the new root form to the dictionary
        for further usage. The method first searches the suffix trie for the reverse string of the surface form. This
        way, it can identify if the word has a suffix that is in the most frequently used suffix list. Since a word can
        have multiple possible suffixes, the method identifies the longest suffix and returns the substring of the
        surface form tht does not contain the suffix. Let say the word is 'googlelaştırdık', it will identify 'tık' as
        a suffix and will return 'googlelaştır' as a possible root form. Another example will be 'homelesslerimizle', it
        will identify 'lerimizle' as suffix and will return 'homeless' as a possible root form. If the root word ends
        with 'ğ', it is replacesd with 'k'. 'morfolojikliğini' will return 'morfolojikliğ' then which will be replaced
        with 'morfolojiklik'.
        :param surfaceForm: Surface form for which we will identify a possible new root form.
        :return: Possible new root form.
        """
        words = self.__suffix_trie.getWordsWithPrefix(self.reverseString(surfaceForm))
        candidate_list = []
        for word in words:
            candidate_word = surfaceForm[0: len(surfaceForm) - len(word.getName())]
            if candidate_word.endswith("ğ"):
                candidate_word = candidate_word[0: len(candidate_word) - 1] + "k"
                new_word = TxtWord(candidate_word, "CL_ISIM")
                new_word.addFlag("IS_SD")
            else:
                new_word = TxtWord(candidate_word, "CL_ISIM")
                new_word.addFlag("CL_FIIL")
            candidate_list.append(new_word)
            self.__dictionary_trie.addWord(candidate_word, new_word)
        return candidate_list

    def robustMorphologicalAnalysis(self, sentenceOrSurfaceForm):
        """
        The robustMorphologicalAnalysis is used to analyse surfaceForm String. First it gets the currentParse of the
        surfaceForm then, if the size of the currentParse is 0, and given surfaceForm is a proper noun, it adds the
        surfaceForm whose state name is ProperRoot to an list, of it is not a proper noon, it adds the surfaceForm
        whose state name is NominalRoot to the list.
        The robustMorphologicalAnalysis method takes just one argument as an input. It gets the name of the words from
        input sentence then calls robustMorphologicalAnalysis with surfaceForm.

        PARAMETERS
        ----------
        sentenceOrSurfaceForm
            Sentence type input used to get surfaceForm.
            String to analyse.

        RETURNS
        -------
        list
            FsmParseList array which holds the result of the analysis.
        FsmParseList
            FsmParseList type currentParse which holds morphological analysis of the surfaceForm.
        """
        if isinstance(sentenceOrSurfaceForm, Sentence):
            sentence = sentenceOrSurfaceForm
            result = []
            for i in range(sentence.wordCount()):
                original_form = sentence.getWord(i).getName()
                spell_corrected_form = self.__dictionary.getCorrectForm(original_form)
                if len(spell_corrected_form) == 0:
                    spell_corrected_form = original_form
                word_fsm_parse_list = self.robustMorphologicalAnalysis(spell_corrected_form)
                result.append(word_fsm_parse_list)
            return result
        elif isinstance(sentenceOrSurfaceForm, str):
            surface_form = sentenceOrSurfaceForm
            if surface_form is None or len(surface_form) == 0:
                return FsmParseList([])
            current_parse = self.morphologicalAnalysis(surface_form)
            if current_parse.size() == 0:
                fsm_parse = []
                if self.isProperNoun(surface_form):
                    fsm_parse.append(FsmParse(surface_form, self.__finite_state_machine.getState("ProperRoot")))
                if self.__isCode(surface_form):
                    fsm_parse.append(FsmParse(surface_form, self.__finite_state_machine.getState("CodeRoot")))
                new_candidate_list = self.rootOfPossiblyNewWord(surface_form)
                if len(new_candidate_list) != 0:
                    for word in new_candidate_list:
                        fsm_parse.append(FsmParse(word, self.__finite_state_machine.getState("VerbalRoot")))
                        fsm_parse.append(FsmParse(word, self.__finite_state_machine.getState("NominalRoot")))
                fsm_parse.append(FsmParse(surface_form, self.__finite_state_machine.getState("NominalRoot")))
                return FsmParseList(self.__parseWord(fsm_parse, surface_form))
            else:
                return current_parse

    def __isInteger(self, surfaceForm: str) -> bool:
        """
        The isInteger method compares input surfaceForm with given regex and returns the result.
        Supports positive integer checks only.

        PARAMETERS
        ----------
        surfaceForm : str
            String to check.

        RETURNS
        -------
        bool
            True if surfaceForm matches with the regex.
        """
        if not self.patternMatches("[+-]?\\d+", surfaceForm):
            return False
        length = len(surfaceForm)
        if length < 10:
            return True
        elif length > 10:
            return False
        else:
            return surfaceForm <= "2147483647"

    def __isDouble(self, surfaceForm: str) -> bool:
        """
        The isDouble method compares input surfaceForm with given regex and returns the result.

        PARAMETERS
        ----------
        surfaceForm : str
            String to check.

        RETURNS
        -------
        bool
            True if surfaceForm matches with the regex.
        """
        return self.patternMatches("[+-]?(\\d+)?\\.\\d*", surfaceForm)

    def __isNumber(self, surfaceForm: str) -> bool:
        """
        The isNumber method compares input surfaceForm with the array of written numbers and returns the result.

        PARAMETERS
        ----------
        surfaceForm : str
            String to check.

        RETURNS
        -------
        bool
            True if surfaceForm matches with the regex.
        """
        numbers = ["bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz",
                   "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan",
                   "yüz", "bin", "milyon", "milyar", "trilyon", "katrilyon"]
        word = surfaceForm
        count = 0
        while len(word) > 0:
            found = False
            for number in numbers:
                if word.startswith(number):
                    found = True
                    count = count + 1
                    word = word[len(number):]
                    break
            if not found:
                break
        return len(word) == 0 and count > 1

    def __toLower(self, surfaceForm: str) -> str:
        """
        Converts a word to its lower form.
        :param surfaceForm: Surface form to convert.
        :return: Lowered surface form.
        """
        if "I" in surfaceForm or "İ" in surfaceForm:
            result = ""
            for i in range(len(surfaceForm)):
                if surfaceForm[i] == "I":
                    result = result + "ı"
                elif surfaceForm[i] == "İ":
                    result = result + "i"
                else:
                    result = result + surfaceForm[i].lower()
            return result
        else:
            return surfaceForm.lower()

    def morphologicalAnalysisExists(self,
                                    rootWord: TxtWord,
                                    surfaceForm: str) -> bool:
        """
        The morphologicalAnalysisExists method calls analysisExists to check the existence of the analysis with given
        root and surfaceForm.

        PARAMETERS
        ----------
        surfaceForm : str
            String to check.
        rootWord : TxtWord
            TxtWord input root.

        RETURNS
        -------
        bool
            True an analysis exists, otherwise return False.
        """
        return self.__analysisExists(rootWord, self.__toLower(surfaceForm), True)
