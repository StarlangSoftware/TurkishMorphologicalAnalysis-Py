import copy
import re

from Corpus.Sentence import Sentence
from DataStructure.Cache.LRUCache import LRUCache
from Dictionary.Trie.Trie import Trie
from Dictionary.TxtDictionary import TxtDictionary
from Dictionary.TxtWord import TxtWord
from Dictionary.Word import Word

from MorphologicalAnalysis.FiniteStateMachine import FiniteStateMachine
from MorphologicalAnalysis.FsmParse import FsmParse
from MorphologicalAnalysis.FsmParseList import FsmParseList
from MorphologicalAnalysis.MetamorphicParse import MetamorphicParse
from MorphologicalAnalysis.MorphologicalParse import MorphologicalParse
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag
from MorphologicalAnalysis.State import State
from MorphologicalAnalysis.Transition import Transition


class FsmMorphologicalAnalyzer:
    __dictionaryTrie: Trie
    __finiteStateMachine: FiniteStateMachine
    __dictionary: TxtDictionary
    __cache: LRUCache
    __mostUsedPatterns = {}
    __parsedSurfaceForms = None

    MAX_DISTANCE = 2

    def __init__(self, dictionaryFileName=None, misspelledFileName=None, fileName="turkish_finite_state_machine.xml",
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
        self.__finiteStateMachine = FiniteStateMachine(fileName)
        self.__dictionaryTrie = self.__dictionary.prepareTrie()
        self.__cache = LRUCache(cacheSize)

    def addParsedSurfaceForms(self, fileName: str):
        self.__parsedSurfaceForms = set()
        file = open(fileName, "r")
        lines = file.readlines()
        for line in lines:
            self.__parsedSurfaceForms.add(line.strip())

    def getPossibleWords(self, morphologicalParse: MorphologicalParse, metamorphicParse: MetamorphicParse) -> set:
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
        isRootVerb = morphologicalParse.getRootPos() == "VERB"
        containsVerb = morphologicalParse.containsTag(MorphologicalTag.VERB)
        verbTransition = Transition("mAk")
        result = set()
        if metamorphicParse is None or metamorphicParse.getWord() is None:
            return result
        currentWord = metamorphicParse.getWord().getName()
        pluralIndex = -1
        compoundWord = self.__dictionaryTrie.getCompundWordStartingWith(currentWord)
        if not isRootVerb:
            if compoundWord is not None and len(compoundWord.getName()) - len(currentWord) < 3:
                result.add(compoundWord.getName())
            result.add(currentWord)
        currentRoot = self.__dictionary.getWord(metamorphicParse.getWord().getName())
        if currentRoot is None and compoundWord is not None:
            currentRoot = compoundWord
        if currentRoot is not None:
            if isRootVerb:
                verbWord = verbTransition.makeTransitionNoStartState(currentRoot, currentWord)
                result.add(verbWord)
            pluralWord = None
            for i in range(1, metamorphicParse.size()):
                transition = Transition(metamorphicParse.getMetaMorpheme(i))
                if metamorphicParse.getMetaMorpheme(i) == "lAr":
                    pluralWord = currentWord
                    pluralIndex = i + 1
                currentWord = transition.makeTransitionNoStartState(currentRoot, currentWord)
                result.add(currentWord)
                if containsVerb:
                    verbWord = verbTransition.makeTransitionNoStartState(currentRoot, currentWord)
                    result.add(verbWord)
            if pluralWord is not None:
                currentWord = pluralWord
                for i in range(pluralIndex, metamorphicParse.size()):
                    transition = Transition(metamorphicParse.getMetaMorpheme(i))
                    currentWord = transition.makeTransitionNoStartState(currentRoot, currentWord)
                    result.add(currentWord)
                    if containsVerb:
                        verbWord = verbTransition.makeTransitionNoStartState(currentRoot, currentWord)
                        result.add(verbWord)
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
        return self.__finiteStateMachine

    def __isPossibleSubstring(self, shortString: str, longString: str, root: TxtWord) -> bool:
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
        rootWord = shortString == root.getName() or longString == root.getName()
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
        if rootWord and (root.getName() == "ben" or root.lastIdropsDuringSuffixation()
                         or root.lastIdropsDuringPassiveSuffixation()):
            return distance <= self.MAX_DISTANCE
        elif shortString.endswith("e") or shortString.endswith("a") or shortString.endswith("p") \
                or shortString.endswith("ç") or shortString.endswith("t") or shortString.endswith("k") \
                or (rootWord and (root.rootSoftenDuringSuffixation() or root.vowelEChangesToIDuringYSuffixation()
                                  or root.vowelAChangesToIDuringYSuffixation() or root.endingKChangesIntoG())):
            return last != 2 and distance <= self.MAX_DISTANCE - 1
        else:
            return distance <= self.MAX_DISTANCE - 2

    def __initializeParseList(self, fsmParse: list, root: TxtWord, isProper: bool):
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
            currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("NominalRootPlural"))
            fsmParse.append(currentFsmParse)
        elif root.isPortmanteauEndingWithSI():
            currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 2],
                                       self.__finiteStateMachine.getState("CompoundNounRoot"))
            fsmParse.append(currentFsmParse)
            currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("NominalRootNoPossesive"))
            fsmParse.append(currentFsmParse)
        elif root.isPortmanteau():
            if root.isPortmanteauFacedVowelEllipsis():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("NominalRootNoPossesive"))
                fsmParse.append(currentFsmParse)
                currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 2] +
                                           root.getName()[len(root.getName()) - 1] +
                                           root.getName()[len(root.getName()) - 2],
                                           self.__finiteStateMachine.getState("CompoundNounRoot"))
            elif root.isPortmanteauFacedSoftening():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("NominalRootNoPossesive"))
                fsmParse.append(currentFsmParse)
                if root.getName()[len(root.getName()) - 2] == "b":
                    currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 2] + "p",
                                               self.__finiteStateMachine.getState("CompoundNounRoot"))
                elif root.getName()[len(root.getName()) - 2] == "c":
                    currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 2] + "ç",
                                               self.__finiteStateMachine.getState("CompoundNounRoot"))
                elif root.getName()[len(root.getName()) - 2] == "d":
                    currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 2] + "t",
                                               self.__finiteStateMachine.getState("CompoundNounRoot"))
                elif root.getName()[len(root.getName()) - 2] == "ğ":
                    currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 2] + "k",
                                               self.__finiteStateMachine.getState("CompoundNounRoot"))
                else:
                    currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 1],
                                               self.__finiteStateMachine.getState("CompoundNounRoot"))
            else:
                currentFsmParse = FsmParse(root.getName()[:len(root.getName()) - 1],
                                           self.__finiteStateMachine.getState("CompoundNounRoot"))
            fsmParse.append(currentFsmParse)
        else:
            if root.isHeader():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("HeaderRoot"))
                fsmParse.append(currentFsmParse)
            if root.isInterjection():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("InterjectionRoot"))
                fsmParse.append(currentFsmParse)
            if root.isDuplicate():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("DuplicateRoot"))
                fsmParse.append(currentFsmParse)
            if root.isNumeral():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("CardinalRoot"))
                fsmParse.append(currentFsmParse)
            if root.isReal():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("RealRoot"))
                fsmParse.append(currentFsmParse)
            if root.isFraction():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("FractionRoot"))
                fsmParse.append(currentFsmParse)
            if root.isDate():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("DateRoot"))
                fsmParse.append(currentFsmParse)
            if root.isPercent():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PercentRoot"))
                fsmParse.append(currentFsmParse)
            if root.isRange():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("RangeRoot"))
                fsmParse.append(currentFsmParse)
            if root.isTime():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("TimeRoot"))
                fsmParse.append(currentFsmParse)
            if root.isOrdinal():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("OrdinalRoot"))
                fsmParse.append(currentFsmParse)
            if root.isVerb() or root.isPassive():
                if root.verbType() != "":
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("VerbalRoot("
                                                                                        + root.verbType() + ")"))
                elif not root.isPassive():
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("VerbalRoot"))
                else:
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PassiveHn"))
                fsmParse.append(currentFsmParse)
            if root.isPronoun():
                if root.getName() == "kendi":
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PronounRoot(REFLEX)"))
                    fsmParse.append(currentFsmParse)
                if root.getName() == "öbür" or root.getName() == "öteki" or root.getName() == "hep" or \
                        root.getName() == "kimse" or root.getName() == "diğeri" or root.getName() == "hiçbiri" or \
                        root.getName() == "böylesi" or root.getName() == "birbiri" or root.getName() == "birbirleri" or\
                        root.getName() == "biri" or root.getName() == "başkası" or root.getName() == "bazı" or \
                        root.getName() == "kimi":
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PronounRoot(QUANT)"))
                    fsmParse.append(currentFsmParse)
                if root.getName() == "tümü" or root.getName() == "topu" or root.getName() == "herkes" or \
                        root.getName() == "cümlesi" or root.getName() == "çoğu" or root.getName() == "birçoğu" or \
                        root.getName() == "birkaçı" or root.getName() == "birçokları" or root.getName() == "hepsi":
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PronounRoot(QUANTPLURAL)"))
                    fsmParse.append(currentFsmParse)
                if root.getName() == "o" or root.getName() == "bu" or root.getName() == "şu":
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PronounRoot(DEMONS)"))
                    fsmParse.append(currentFsmParse)
                if root.getName() == "ben" or root.getName() == "sen" or root.getName() == "o" or \
                        root.getName() == "biz" or root.getName() == "siz" or root.getName() == "onlar":
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PronounRoot(PERS)"))
                    fsmParse.append(currentFsmParse)
                if root.getName() == "nere" or root.getName() == "ne" or root.getName() == "kaçı" or \
                        root.getName() == "kim" or root.getName() == "hangi":
                    currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PronounRoot(QUES)"))
                    fsmParse.append(currentFsmParse)
            if root.isAdjective():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("AdjectiveRoot"))
                fsmParse.append(currentFsmParse)
            if root.isPureAdjective():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("Adjective"))
                fsmParse.append(currentFsmParse)
            if root.isNominal():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("NominalRoot"))
                fsmParse.append(currentFsmParse)
            if root.isAbbreviation():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("NominalRoot"))
                fsmParse.append(currentFsmParse)
            if root.isProperNoun() and isProper:
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("ProperRoot"))
                fsmParse.append(currentFsmParse)
            if root.isQuestion():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("QuestionRoot"))
                fsmParse.append(currentFsmParse)
            if root.isDeterminer():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("DeterminerRoot"))
                fsmParse.append(currentFsmParse)
            if root.isConjunction():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("ConjunctionRoot"))
                fsmParse.append(currentFsmParse)
            if root.isPostP():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("PostP"))
                fsmParse.append(currentFsmParse)
            if root.isAdverb():
                currentFsmParse = FsmParse(root, self.__finiteStateMachine.getState("AdverbRoot"))
                fsmParse.append(currentFsmParse)

    def __initializeParseListFromRoot(self, parseList: list, root: TxtWord, isProper: bool):
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
            newRoot = copy.deepcopy(root)
            newRoot.removeFlag("IS_UU")
            newRoot.removeFlag("IS_UUU")
            self.__initializeParseList(parseList, newRoot, isProper)
        if root.rootSoftenAndNotSoftenDuringSuffixation():
            newRoot = copy.deepcopy(root)
            newRoot.removeFlag("IS_SD")
            newRoot.removeFlag("IS_SDD")
            self.__initializeParseList(parseList, newRoot, isProper)
        if root.lastIDropsAndNotDropDuringSuffixation():
            newRoot = copy.deepcopy(root)
            newRoot.removeFlag("IS_UD")
            newRoot.removeFlag("IS_UDD")
            self.__initializeParseList(parseList, newRoot, isProper)
        if root.duplicatesAndNotDuplicatesDuringSuffixation():
            newRoot = copy.deepcopy(root)
            newRoot.removeFlag("IS_ST")
            newRoot.removeFlag("IS_STT")
            self.__initializeParseList(parseList, newRoot, isProper)
        if root.endingKChangesIntoG() and root.containsFlag("IS_OA"):
            newRoot = copy.deepcopy(root)
            newRoot.removeFlag("IS_OA")
            self.__initializeParseList(parseList, newRoot, isProper)

    def __initializeParseListFromSurfaceForm(self, surfaceForm: str, isProper: bool) -> list:
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
        initialFsmParse = []
        if len(surfaceForm) == 0:
            return initialFsmParse
        words = self.__dictionaryTrie.getWordsWithPrefix(surfaceForm)
        for word in words:
            self.__initializeParseListFromRoot(initialFsmParse, word, isProper)
        return initialFsmParse

    def __addNewParsesFromCurrentParse(self, currentFsmParse: FsmParse, fsmParse: list, maxLengthOrSurfaceForm,
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
        currentState = currentFsmParse.getFinalSuffix()
        currentSurfaceForm = currentFsmParse.getSurfaceForm()
        if isinstance(maxLengthOrSurfaceForm, int):
            maxLength = maxLengthOrSurfaceForm
            for currentTransition in self.__finiteStateMachine.getTransitions(currentState):
                if currentTransition.transitionPossibleForParse(currentFsmParse) \
                        and (currentSurfaceForm != root.getName()
                             or (currentSurfaceForm == root.getName() and
                                 currentTransition.transitionPossibleWord(root, currentState))):
                    tmp = currentTransition.makeTransition(root, currentSurfaceForm, currentFsmParse.getStartState())
                    if len(tmp) <= maxLength:
                        newFsmParse = copy.deepcopy(currentFsmParse)
                        newFsmParse.addSuffix(currentTransition.toState(), tmp, currentTransition.withName(),
                                              currentTransition.__str__(), currentTransition.toPos())
                        newFsmParse.setAgreement(currentTransition.withName())
                        fsmParse.append(newFsmParse)
        elif isinstance(maxLengthOrSurfaceForm, str):
            surfaceForm = maxLengthOrSurfaceForm
            for currentTransition in self.__finiteStateMachine.getTransitions(currentState):
                if currentTransition.transitionPossibleForString(currentFsmParse.getSurfaceForm(), surfaceForm) and \
                        currentTransition.transitionPossibleForParse(currentFsmParse) and (
                        currentSurfaceForm != root.getName()
                        or (currentSurfaceForm == root.getName() and
                            currentTransition.transitionPossibleForWord(root, currentState))):
                    tmp = currentTransition.makeTransition(root, currentSurfaceForm, currentFsmParse.getStartState())
                    if (len(tmp) < len(surfaceForm) and self.__isPossibleSubstring(tmp, surfaceForm, root)) or \
                            (len(tmp) == len(surfaceForm) and (
                                    root.lastIdropsDuringSuffixation() or tmp == surfaceForm)):
                        newFsmParse = copy.deepcopy(currentFsmParse)
                        newFsmParse.addSuffix(currentTransition.toState(), tmp, currentTransition.withName(),
                                              currentTransition.__str__(), currentTransition.toPos())
                        newFsmParse.setAgreement(currentTransition.withName())
                        fsmParse.append(newFsmParse)

    def __parseExists(self, fsmParse: list, surfaceForm: str) -> bool:
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
            currentFsmParse = fsmParse.pop(0)
            root = currentFsmParse.getWord()
            currentState = currentFsmParse.getFinalSuffix()
            currentSurfaceForm = currentFsmParse.getSurfaceForm()
            if currentState.isEndState() and currentSurfaceForm == surfaceForm:
                return True
            self.__addNewParsesFromCurrentParse(currentFsmParse, fsmParse, surfaceForm, root)
        return False

    def __parseWord(self, fsmParse: list, maxLengthOrSurfaceForm) -> list:
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
        if isinstance(maxLengthOrSurfaceForm, int):
            maxLength = maxLengthOrSurfaceForm
            while len(fsmParse) > 0:
                currentFsmParse = fsmParse.pop(0)
                root = currentFsmParse.getWord()
                currentState = currentFsmParse.getFinalSuffix()
                currentSurfaceForm = currentFsmParse.getSurfaceForm()
                if currentState.isEndState() and len(currentSurfaceForm) <= maxLength:
                    exists = False
                    for i in range(len(result)):
                        if currentFsmParse.suffixList() == result[i].suffixList():
                            exists = True
                            break
                    if not exists:
                        result.append(currentFsmParse)
                        currentFsmParse.constructInflectionalGroups()
                self.__addNewParsesFromCurrentParse(currentFsmParse, fsmParse, maxLength, root)
        elif isinstance(maxLengthOrSurfaceForm, str):
            surfaceForm = maxLengthOrSurfaceForm
            while len(fsmParse) > 0:
                currentFsmParse = fsmParse.pop(0)
                root = currentFsmParse.getWord()
                currentState = currentFsmParse.getFinalSuffix()
                currentSurfaceForm = currentFsmParse.getSurfaceForm()
                if currentState.isEndState() and currentSurfaceForm == surfaceForm:
                    exists = False
                    for i in range(len(result)):
                        if currentFsmParse.suffixList() == result[i].suffixList():
                            exists = True
                            break
                    if not exists:
                        result.append(currentFsmParse)
                        currentFsmParse.constructInflectionalGroups()
                self.__addNewParsesFromCurrentParse(currentFsmParse, fsmParse, surfaceForm, root)
        return result

    def morphologicalAnalysisRoot(self, surfaceForm: str, root: TxtWord, state=None) -> list:
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
            initialFsmParse = []
            self.__initializeParseListFromRoot(initialFsmParse, root, self.isProperNoun(surfaceForm))
        else:
            initialFsmParse = [FsmParse(root, self.__finiteStateMachine.getState(state))]
        return self.__parseWord(initialFsmParse, surfaceForm)

    def generateAllParses(self, root: TxtWord, maxLength: int) -> list:
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
        initialFsmParse = []
        if root.isProperNoun():
            self.__initializeParseListFromRoot(initialFsmParse, root, True)
        self.__initializeParseListFromRoot(initialFsmParse, root, False)
        return self.__parseWord(initialFsmParse, maxLength)

    def __analysisExists(self, rootWord: TxtWord, surfaceForm: str, isProper: bool) -> bool:
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
            initialFsmParse = []
            self.__initializeParseListFromRoot(initialFsmParse, rootWord, isProper)
        else:
            initialFsmParse = self.__initializeParseListFromSurfaceForm(surfaceForm, isProper)
        return self.__parseExists(initialFsmParse, surfaceForm)

    def __analysis(self, surfaceForm: str, isProper: bool) -> list:
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
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("Punctuation", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.__isNumber(surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("CardinalRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.patternMatches("(\\d\\d|\\d)/(\\d\\d|\\d)/\\d+", surfaceForm) or \
                self.patternMatches("(\\d\\d|\\d)\\.(\\d\\d|\\d)\\.\\d+", surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("DateRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.patternMatches("\\d+/\\d+", surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("FractionRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            fsmParse = FsmParse(surfaceForm, State("DateRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.patternMatches("\\d+\\\\/\\d+", surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("FractionRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if surfaceForm == "%" or self.patternMatches("%(\\d\\d|\\d)", surfaceForm) or \
                self.patternMatches("%(\\d\\d|\\d)\\.\\d+", surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("PercentRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d):(\\d\\d|\\d)", surfaceForm) or \
                self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d)", surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("TimeRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.patternMatches("\\d+-\\d+", surfaceForm) or \
                self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d)-(\\d\\d|\\d):(\\d\\d|\\d)", surfaceForm) or \
                self.patternMatches("(\\d\\d|\\d)\\.(\\d\\d|\\d)-(\\d\\d|\\d)\\.(\\d\\d|\\d)", surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("RangeRoot", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if surfaceForm.startswith("#"):
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("Hashtag", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if "@" in surfaceForm:
            initialFsmParse = []
            fsmParse = FsmParse(surfaceForm, State("Email", True, True))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if surfaceForm.endswith(".") and self.__isInteger(surfaceForm[:len(surfaceForm) - 1]):
            initialFsmParse = []
            fsmParse = FsmParse(int(surfaceForm[:len(surfaceForm) - 1]),
                                self.__finiteStateMachine.getState("OrdinalRoot"))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.__isInteger(surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(int(surfaceForm), self.__finiteStateMachine.getState("CardinalRoot"))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        if self.__isDouble(surfaceForm):
            initialFsmParse = []
            fsmParse = FsmParse(float(surfaceForm), self.__finiteStateMachine.getState("RealRoot"))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        initialFsmParse = self.__initializeParseListFromSurfaceForm(surfaceForm, isProper)
        return self.__parseWord(initialFsmParse, surfaceForm)

    def patternMatches(self, expr: str, value: str) -> bool:
        if expr in self.__mostUsedPatterns:
            return self.__mostUsedPatterns[expr].fullmatch(value) is not None
        else:
            compiledExpression = re.compile(expr)
            self.__mostUsedPatterns[expr] = compiledExpression
            return compiledExpression.fullmatch(value) is not None

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
                originalForm = sentence.getWord(i).getName()
                spellCorrectedForm = self.__dictionary.getCorrectForm(originalForm)
                if len(spellCorrectedForm) == 0:
                    spellCorrectedForm = originalForm
                wordFsmParseList = self.morphologicalAnalysis(spellCorrectedForm)
                result.append(wordFsmParseList)
            return result
        elif isinstance(sentenceOrSurfaceForm, str):
            surfaceForm = sentenceOrSurfaceForm
            if self.__parsedSurfaceForms is not None and surfaceForm not in self.__parsedSurfaceForms:
                return FsmParseList([])
            if self.__cache.contains(surfaceForm):
                return self.__cache.get(surfaceForm)
            if self.patternMatches("(\\w|Ç|Ş|İ|Ü|Ö)\\.", surfaceForm):
                self.__dictionaryTrie.addWord(self.__toLower(surfaceForm), TxtWord(self.__toLower(surfaceForm), "IS_OA"))
            defaultFsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
            if len(defaultFsmParse) > 0:
                fsmParseList = FsmParseList(defaultFsmParse)
                self.__cache.add(surfaceForm, fsmParseList)
                return fsmParseList
            fsmParse = []
            if "'" in surfaceForm:
                possibleRoot = surfaceForm[:surfaceForm.index('\'')]
                if len(possibleRoot) > 0:
                    if "/" in possibleRoot or "\\/" in possibleRoot:
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_KESIR"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif self.patternMatches("(\\d\\d|\\d)/(\\d\\d|\\d)/\\d+", possibleRoot) or \
                            self.patternMatches("(\\d\\d|\\d)\\.(\\d\\d|\\d)\\.\\d+", possibleRoot):
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_DATE"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif self.patternMatches("\\d+/\\d+", possibleRoot):
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_KESIR"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif self.patternMatches("%(\\d\\d|\\d)", possibleRoot) or \
                            self.patternMatches("%(\\d\\d|\\d)\\.\\d+", possibleRoot):
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_PERCENT"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d):(\\d\\d|\\d)", possibleRoot) or \
                            self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d)", possibleRoot):
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_ZAMAN"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif self.patternMatches("\\d+-\\d+", possibleRoot) or \
                            self.patternMatches("(\\d\\d|\\d):(\\d\\d|\\d)-(\\d\\d|\\d):(\\d\\d|\\d)", possibleRoot) or\
                            self.patternMatches("(\\d\\d|\\d)\\.(\\d\\d|\\d)-(\\d\\d|\\d)\\.(\\d\\d|\\d)",
                                                possibleRoot):
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_RANGE"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif self.__isInteger(possibleRoot):
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_SAYI"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif self.__isDouble(possibleRoot):
                        self.__dictionaryTrie.addWord(possibleRoot, TxtWord(possibleRoot, "IS_REELSAYI"))
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                    elif Word.isCapital(possibleRoot):
                        newWord = None
                        word = self.__dictionary.getWord(self.__toLower(possibleRoot))
                        if word is not None and isinstance(word, TxtWord):
                            word.addFlag("IS_OA")
                        else:
                            newWord = TxtWord(self.__toLower(possibleRoot), "IS_OA")
                            self.__dictionaryTrie.addWord(self.__toLower(possibleRoot), newWord)
                        fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
                        if len(fsmParse) == 0 and newWord is not None:
                            newWord.addFlag("IS_KIS")
                            fsmParse = self.__analysis(self.__toLower(surfaceForm), self.isProperNoun(surfaceForm))
            fsmParseList = FsmParseList(fsmParse)
            if fsmParseList.size() > 0:
                self.__cache.add(surfaceForm, fsmParseList)
            return fsmParseList

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
                originalForm = sentence.getWord(i).getName()
                spellCorrectedForm = self.__dictionary.getCorrectForm(originalForm)
                if len(spellCorrectedForm) == 0:
                    spellCorrectedForm = originalForm
                wordFsmParseList = self.robustMorphologicalAnalysis(spellCorrectedForm)
                result.append(wordFsmParseList)
            return result
        elif isinstance(sentenceOrSurfaceForm, str):
            surfaceForm = sentenceOrSurfaceForm
            if surfaceForm is None or len(surfaceForm) == 0:
                return FsmParseList([])
            currentParse = self.morphologicalAnalysis(surfaceForm)
            if currentParse.size() == 0:
                fsmParse = []
                if self.isProperNoun(surfaceForm):
                    fsmParse.append(FsmParse(surfaceForm, self.__finiteStateMachine.getState("ProperRoot")))
                    return FsmParseList(self.__parseWord(fsmParse, surfaceForm))
                else:
                    fsmParse.append(FsmParse(surfaceForm, self.__finiteStateMachine.getState("NominalRoot")))
                    return FsmParseList(self.__parseWord(fsmParse, surfaceForm))
            else:
                return currentParse

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
        if not self.patternMatches("\\+?\\d+", surfaceForm):
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
        return self.patternMatches("\\+?(\\d+)?\\.\\d*", surfaceForm)

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

    def morphologicalAnalysisExists(self, rootWord: TxtWord, surfaceForm: str) -> bool:
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
