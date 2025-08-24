from Dictionary.TxtWord import TxtWord
from Dictionary.Word import Word
from Language.TurkishLanguage import TurkishLanguage

from MorphologicalAnalysis.FsmParse import FsmParse
from MorphologicalAnalysis.MorphotacticEngine import MorphotacticEngine
from MorphologicalAnalysis.State import State


class Transition:

    __to_state: State
    __with: str
    __with_name: str
    __to_pos: str

    def __init__(self,
                 _with: str,
                 toState=None,
                 withName=None,
                 toPos=None):
        """
        Constructor of Transition class which takes a State, and three str as input. Then it
        initializes toState, with, withName and toPos variables with given inputs.

        PARAMETERS
        ----------
        _with : str
            String input.
        toState : State
            State input.
        withName : str
            String input.
        toPos : str
            String input.
        """
        self.__with = _with
        self.__to_state = toState
        self.__with_name = withName
        self.__to_pos = toPos

    def toState(self) -> State:
        """
        Getter for the toState variable.

        RETURNS
        -------
        State
            toState variable.
        """
        return self.__to_state

    def toPos(self) -> str:
        """
        Getter for the toPos variable.

        RETURNS
        -------
        str
            toPos variable.
        """
        return self.__to_pos

    def transitionPossibleForString(self,
                                    currentSurfaceForm: str,
                                    realSurfaceForm: str) -> bool:
        """
        The transitionPossibleForString method takes two str as inputs; currentSurfaceForm and realSurfaceForm. If the
        length of the given currentSurfaceForm is greater than the given realSurfaceForm, it directly returns true. If
        not, it takes a substring from given realSurfaceForm with the size of currentSurfaceForm. Then checks for the
        characters of with variable.

        If the character of with that makes transition is C, it returns true if the substring contains c or ç.
        If the character of with that makes transition is D, it returns true if the substring contains d or t.
        If the character of with that makes transition is A, it returns true if the substring contains a or e.
        If the character of with that makes transition is K, it returns true if the substring contains k, g or ğ.
        If the character of with that makes transition is other than the ones above, it returns true if the substring
        contains the same character as with.

        PARAMETERS
        ----------
        currentSurfaceForm : str
            String input.
        realSurfaceForm : str
            String input.

        RETURNS
        -------
        bool
            True when the transition is possible according to Turkish grammar, False otherwise.
        """
        if len(currentSurfaceForm) == 0 or len(currentSurfaceForm) >= len(realSurfaceForm):
            return True
        search_string = realSurfaceForm[len(currentSurfaceForm):]
        for ch in self.__with:
            if ch == 'C':
                return 'c' in search_string or 'ç' in search_string
            elif ch == 'D':
                return 'd' in search_string or 't' in search_string
            elif ch == 'c' or ch == 'e' or ch == 'r' or ch == 'p' or ch == 'l' or ch == 'b' or ch == 'd' or ch == 'g' \
                    or ch == 'o' or ch == 'm' or ch == 'v' or ch == 'i' or ch == 'ü' or ch == 'z':
                return ch in search_string
            elif ch == 'A':
                return 'a' in search_string or 'e' in search_string
            elif ch == 'k':
                return 'k' in search_string or 'g' in search_string or 'ğ' in search_string
        return True

    def transitionPossibleForParse(self, currentFsmParse: FsmParse) -> bool:
        """
        The transitionPossibleForParse method takes a FsmParse currentFsmParse as an input. It then checks some special
        cases;

        PARAMETERS
        ----------
        currentFsmParse : FsmParse
            Parse to be checked

        RETURNS
        -------
        bool
            True if transition is possible False otherwise
        """
        if self.__with == "Ar" and currentFsmParse.getSurfaceForm().endswith("l") and \
                currentFsmParse.getWord().getName() != currentFsmParse.getSurfaceForm():
            return False
        if currentFsmParse.getVerbAgreement() is not None and currentFsmParse.getPossesiveAgreement() is not None and \
                self.__with_name is not None:
            if currentFsmParse.getVerbAgreement() == "A3PL" and self.__with_name == "^DB+VERB+ZERO+PRES+A1SG":
                return False
            if currentFsmParse.getVerbAgreement() == "A3SG" and (currentFsmParse.getPossesiveAgreement() == "P1SG" or
                                                                 currentFsmParse.getPossesiveAgreement() == "P2SG") \
                    and self.__with_name == "^DB+VERB+ZERO+PRES+A1PL":
                return False
        return True

    def transitionPossibleForWord(self,
                                  root: TxtWord,
                                  fromState: State) -> bool:
        """
        The transitionPossible method takes root and current parse as inputs. It then checks some special cases.
        :param root: Current root word
        :param fromState: From which state we arrived to this state.
        :return: true if transition is possible false otherwise
        """
        if root.isAdjective() and ((root.isNominal() and not root.isExceptional()) or root.isPronoun()) \
                and self.__to_state.getName() == "NominalRoot(ADJ)" and self.__with == "0":
            return False
        if root.isAdjective() and root.isNominal() and self.__with == "^DB+VERB+ZERO+PRES+A3PL" \
                and fromState.getName() == "AdjectiveRoot":
            return False
        if root.isAdjective() and root.isNominal() and self.__with == "SH" and fromState.getName() == "AdjectiveRoot":
            return False
        if self.__with == "ki":
            return root.takesRelativeSuffixKi()
        if self.__with == "kü":
            return root.takesRelativeSuffixKu()
        if self.__with == "DHr":
            if self.__to_state.getName() == "Adverb":
                return True
            else:
                return root.takesSuffixDIRAsFactitive()
        if self.__with == "Hr" and (
                self.__to_state.getName() == "AdjectiveRoot(VERB)" or self.__to_state.getName() == "OtherTense" or
                self.__to_state.getName() == "OtherTense2"):
            return root.takesSuffixIRAsAorist()
        return True

    def __withFirstChar(self) -> str:
        """
        The withFirstChar method returns the first character of the with variable.

        RETURNS
        -------
        str
            The first character of the with variable.
        """
        if len(self.__with) == 0:
            return "$"
        if self.__with[0] != "'":
            return self.__with[0]
        elif len(self.__with) == 1:
            return self.__with[0]
        else:
            return self.__with[1]

    def __startWithVowelorConsonantDrops(self) -> bool:
        """
        The startWithVowelorConsonantDrops method checks for some cases. If the first character of with variable is
        "nsy", and with variable does not equal to one of the Strings; "ylA, ysA, ymHs, yDH, yken", it returns true. If

        Or, if the first character of with variable is 'A, H: or any other vowels, it returns true.

        RETURNS
        -------
        bool
            True if it starts with vowel or consonant drops, false otherwise.
        """
        if TurkishLanguage.isConsonantDrop(self.__withFirstChar()) and self.__with != "ylA" and self.__with != "ysA" \
                and self.__with != "ymHs" and self.__with != "yDH" and self.__with != "yken":
            return True
        if self.__withFirstChar() == "A" or self.__withFirstChar() == "H" or \
                TurkishLanguage.isVowel(self.__withFirstChar()):
            return True
        return False

    def softenDuringSuffixation(self, root: TxtWord, startState: State) -> bool:
        """
        The startWithVowelorConsonantDrops method checks for some cases. If the first character of with variable is
        "nsy", and with variable does not equal to one of the Strings; "ylA, ysA, ymHs, yDH, yken", it returns true. If

        Or, if the first character of with variable is 'A, H: or any other vowels, it returns true.

        RETURNS
        -------
        bool
            True if it starts with vowel or consonant drops, false otherwise.
        """
        if not startState.getName().startswith("VerbalRoot") and (root.isNominal() or root.isAdjective()) and root.nounSoftenDuringSuffixation() and \
                (self.__with == "Hm" or self.__with == "nDAn" or self.__with == "ncA" or self.__with == "nDA"
                 or self.__with == "yA" or self.__with == "yHm" or self.__with == "yHz" or self.__with == "yH"
                 or self.__with == "nH" or self.__with == "nA" or self.__with == "nHn" or self.__with == "H"
                 or self.__with == "sH" or self.__with == "Hn" or self.__with == "HnHz" or self.__with == "HmHz"):
            return True
        if startState.getName().startswith("VerbalRoot") and root.isVerb() and root.verbSoftenDuringSuffixation() and \
                (self.__with.startswith("Hyor") or self.__with == "yHs" or self.__with == "yAn" or self.__with == "yA"
                 or self.__with == "yAcAk" or self.__with == "yAsH" or self.__with == "yHncA" or self.__with == "yHp"
                 or self.__with == "yAlH" or self.__with == "yArAk" or self.__with == "yAdur" or self.__with == "yHver"
                 or self.__with == "yAgel" or self.__with == "yAgor" or self.__with == "yAbil" or self.__with == "yAyaz"
                 or self.__with == "yAkal" or self.__with == "yAkoy" or self.__with == "yAmA" or self.__with == "yHcH"
                 or self.__with == "yHs" or self.__with == "HCH" or self.__with == "Hr" or self.__with == "Hs"
                 or self.__with == "Hn" or self.__with == "yHn" or self.__with == "yHnHz" or self.__with == "Ar"
                 or self.__with == "Hl"):
            return True
        return False

    def makeTransitionNoStartState(self, root: TxtWord, stem: str) -> str:
        """
        The makeTransition method takes a TxtWord root and s str stem as inputs. If given root is a verb,
        it makes transition with given root and stem with the verbal root state. If given root is not verb, it makes
        transition with given root and stem and the nominal root state.

        PARAMETERS
        ----------
        root : TxtWord
            TxtWord input.
        stem : str
            String input.

        RETURNS
        -------
        str
            String type output that has the transition.
        """
        if root.isVerb():
            return self.makeTransition(root, stem, State("VerbalRoot", True, False))
        else:
            return self.makeTransition(root, stem, State("NominalRoot", True, False))

    def makeTransition(self,
                       root: TxtWord,
                       stem: str,
                       startState: State) -> str:
        """
        The method is main driving method to accomplish the current transition from one state to another depending on
        the root form of the word, current value of the word form, and the type of the start state. The method
        (a) returns the original word form if the transition is an epsilon transition, (b) adds 'nunla' if the current
        stem is 'bu', 'şu' or 'o', (c) returns 'bana' or 'sana' if the current stem is 'ben' or 'sen' respectively.
        For other cases, the method first modifies current stem and then adds the transition using special metamorpheme
        resolving methods. These cases are: (d) Converts 'y' of the first character of the transition to 'i' if the
        current stem is 'ye' or 'de'. (e) Drops the last two characters and adds last character when the transition is
        ('Hl' or 'Hn') and last 'I' drops during passive suffixation. (f) Adds 'y' character when the word ends with 'su'
        and the transition does not start with 'y'. (g) Adds the last character again when the root duplicates during
        suffixation. (h) Drops the last two characters and adds the last character when last 'i' drops during
        suffixation. (i) Replaces the last character with a soft one when the root soften during suffixation.
        :param root: Root of the current word form
        :param stem: Current word form
        :param startState: The state from which this Fsm morphological analysis search has started.
        :return: The current value of the word form after this transition is completed in the finite state machine.
        """
        root_word = root.getName() == stem or (root.getName() + "'") == stem
        formation = stem
        i = 0
        if self.__with == "0":
            return stem
        if (stem == "bu" or stem == "şu" or stem == "o") and root_word and self.__with == "ylA":
            return stem + "nunla"
        if self.__with == "yA":
            if stem == "ben":
                return "bana"
            if stem == "sen":
                return "sana"
        formation_to_check = stem
        if root_word and self.__withFirstChar() == "y" and root.vowelEChangesToIDuringYSuffixation() \
                and (self.__with[1] != "H" or root.getName() == "ye"):
            formation = stem[:len(stem) - 1] + "i"
            formation_to_check = formation
        else:
            if root_word and (self.__with == "Hl" or self.__with == "Hn") and root.lastIdropsDuringPassiveSuffixation():
                formation = stem[:len(stem) - 2] + stem[len(stem) - 1]
                formation_to_check = stem
            else:
                if root_word and root.showsSuRegularities() and self.__startWithVowelorConsonantDrops():
                    formation = stem + 'y'
                    i = 1
                    formation_to_check = formation
                else:
                    if root_word and root.duplicatesDuringSuffixation() and not startState.getName().startswith(
                                    "VerbalRoot") and TurkishLanguage.isConsonantDrop(self.__with[0]):
                        if self.softenDuringSuffixation(root, startState):
                            if Word.lastPhoneme(stem) == "p":
                                formation = stem[:len(stem) - 1] + "bb"
                            elif Word.lastPhoneme(stem) == "t":
                                formation = stem[:len(stem) - 1] + "dd"
                        else:
                            formation = stem + stem[len(stem) - 1]
                        formation_to_check = formation
                    else:
                        if root_word and root.lastIdropsDuringSuffixation() and \
                                not startState.getName().startswith(
                                    "VerbalRoot") and not startState.getName().startswith("ProperRoot") \
                                and self.__startWithVowelorConsonantDrops():
                            if self.softenDuringSuffixation(root, startState):
                                if Word.lastPhoneme(stem) == "p":
                                    formation = stem[:len(stem) - 2] + 'b'
                                elif Word.lastPhoneme(stem) == "t":
                                    formation = stem[:len(stem) - 2] + 'd'
                                elif Word.lastPhoneme(stem) == "ç":
                                    formation = stem[:len(stem) - 2] + 'c'
                            else:
                                formation = stem[:len(stem) - 2] + stem[len(stem) - 1]
                            formation_to_check = stem
                        else:
                            if Word.lastPhoneme(stem) == "p":
                                if self.__startWithVowelorConsonantDrops() and root_word and \
                                        self.softenDuringSuffixation(root, startState):
                                    formation = stem[:len(stem) - 1] + 'b'
                            elif Word.lastPhoneme(stem) == "t":
                                if self.__startWithVowelorConsonantDrops() and root_word and \
                                        self.softenDuringSuffixation(root, startState):
                                    formation = stem[:len(stem) - 1] + 'd'
                            elif Word.lastPhoneme(stem) == "ç":
                                if self.__startWithVowelorConsonantDrops() and root_word and \
                                        self.softenDuringSuffixation(root, startState):
                                    formation = stem[:len(stem) - 1] + 'c'
                            elif Word.lastPhoneme(stem) == "g":
                                if self.__startWithVowelorConsonantDrops() and root_word and \
                                        self.softenDuringSuffixation(root, startState):
                                    formation = stem[:len(stem) - 1] + 'ğ'
                            elif Word.lastPhoneme(stem) == "k":
                                if self.__startWithVowelorConsonantDrops() and root_word and root.endingKChangesIntoG() \
                                        and (not root.isProperNoun() or startState.__str__() != "ProperRoot"):
                                    formation = stem[:len(stem) - 1] + 'g'
                                else:
                                    if self.__startWithVowelorConsonantDrops() and (not root_word or (
                                            self.softenDuringSuffixation(root, startState) and (
                                            not root.isProperNoun() or startState.__str__() != "ProperRoot"))):
                                        formation = stem[:len(stem) - 1] + 'ğ'
                            formation_to_check = formation
        if TurkishLanguage.isConsonantDrop(self.__withFirstChar()) and not TurkishLanguage.isVowel(stem[len(stem) - 1])\
                and (root.isNumeral() or root.isReal() or root.isFraction() or root.isTime() or root.isDate()
                     or root.isPercent() or root.isRange()) \
                and (root.getName().endswith("1") or root.getName().endswith("3") or root.getName().endswith("4")
                     or root.getName().endswith("5") or root.getName().endswith("8") or root.getName().endswith("9")
                     or root.getName().endswith("10") or root.getName().endswith("30") or root.getName().endswith("40")
                     or root.getName().endswith("60") or root.getName().endswith("70") or root.getName().endswith("80")
                     or root.getName().endswith("90") or root.getName().endswith("00")):
            if self.__with[0] == "'":
                formation = formation + "'"
                i = 2
            else:
                i = 1
        else:
            if (TurkishLanguage.isConsonantDrop(self.__withFirstChar()) and TurkishLanguage.isConsonant(
                    Word.lastPhoneme(stem))) or (root_word and root.consonantSMayInsertedDuringPossesiveSuffixation()):
                if self.__with[0] == "'":
                    formation = formation + "'"
                    if root.isAbbreviation():
                        i = 1
                    else:
                        i = 2
                else:
                    i = 1
        while i < len(self.__with):
            if self.__with[i] == "D":
                formation = MorphotacticEngine.resolveD(root, formation, formation_to_check)
            elif self.__with[i] == "A":
                formation = MorphotacticEngine.resolveA(root, formation, root_word, formation_to_check)
            elif self.__with[i] == "H":
                if self.__with[0] != "'":
                    formation = MorphotacticEngine.resolveH(root, formation, i == 0, self.__with.startswith("Hyor"), root_word, formation_to_check)
                else:
                    formation = MorphotacticEngine.resolveH(root, formation, i == 1, False, root_word, formation_to_check)
                root_word = False
            elif self.__with[i] == "C":
                formation = MorphotacticEngine.resolveC(formation, formation_to_check)
            elif self.__with[i] == "S":
                formation = MorphotacticEngine.resolveS(formation)
            elif self.__with[i] == "Ş":
                formation = MorphotacticEngine.resolveSh(formation)
            else:
                if i == len(self.__with) - 1 and self.__with[i] == "s":
                    formation += "ş"
                else:
                    formation += self.__with[i]
            formation_to_check = formation
            i = i + 1
        return formation

    def __str__(self):
        """
        An overridden toString method which returns the with variable.

        RETURNS
        -------
        str
            With variable.
        """
        return self.__with

    def withName(self) -> str:
        """
        The withName method returns the withName variable.

        RETURNS
        -------
        str
            The withName variable.
        """
        return self.__with_name
