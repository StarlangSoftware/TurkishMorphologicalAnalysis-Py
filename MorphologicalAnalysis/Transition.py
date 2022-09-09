from Dictionary.TxtWord import TxtWord
from Dictionary.Word import Word
from Language.TurkishLanguage import TurkishLanguage

from MorphologicalAnalysis.FsmParse import FsmParse
from MorphologicalAnalysis.MorphotacticEngine import MorphotacticEngine
from MorphologicalAnalysis.State import State


class Transition:
    __toState: State
    __with: str
    __withName: str
    __formationToCheck: str
    __toPos: str

    def __init__(self, _with: str, toState=None, withName=None, toPos=None):
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
        self.__toState = toState
        self.__withName = withName
        self.__toPos = toPos

    def toState(self) -> State:
        """
        Getter for the toState variable.

        RETURNS
        -------
        State
            toState variable.
        """
        return self.__toState

    def toPos(self) -> str:
        """
        Getter for the toPos variable.

        RETURNS
        -------
        str
            toPos variable.
        """
        return self.__toPos

    def transitionPossibleForString(self, currentSurfaceForm: str, realSurfaceForm: str) -> bool:
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
        searchString = realSurfaceForm[len(currentSurfaceForm):]
        for ch in self.__with:
            if ch == 'C':
                return 'c' in searchString or 'ç' in searchString
            elif ch == 'D':
                return 'd' in searchString or 't' in searchString
            elif ch == 'c' or ch == 'e' or ch == 'r' or ch == 'p' or ch == 'l' or ch == 'b' or ch == 'd' or ch == 'g' \
                    or ch == 'o' or ch == 'm' or ch == 'v' or ch == 'i' or ch == 'ü' or ch == 'z':
                return ch in searchString
            elif ch == 'A':
                return 'a' in searchString or 'e' in searchString
            elif ch == 'k':
                return 'k' in searchString or 'g' in searchString or 'ğ' in searchString
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
                self.__withName is not None:
            if currentFsmParse.getVerbAgreement() == "A3PL" and self.__withName == "^DB+VERB+ZERO+PRES+A1SG":
                return False
            if currentFsmParse.getVerbAgreement() == "A3SG" and (currentFsmParse.getPossesiveAgreement() == "P1SG" or
                                                                 currentFsmParse.getPossesiveAgreement() == "P2SG") \
                    and self.__withName == "^DB+VERB+ZERO+PRES+A1PL":
                return False
        return True

    def transitionPossibleForWord(self, root: TxtWord, fromState: State) -> bool:
        if root.isAdjective() and ((root.isNominal() and not root.isExceptional()) or root.isPronoun()) \
                and self.__toState.getName() == "NominalRoot(ADJ)" and self.__with == "0":
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
            if self.__toState.getName() == "Adverb":
                return True
            else:
                return root.takesSuffixDIRAsFactitive()
        if self.__with == "Hr" and (
                self.__toState.getName() == "AdjectiveRoot(VERB)" or self.__toState.getName() == "OtherTense" or
                self.__toState.getName() == "OtherTense2"):
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

    def softenDuringSuffixation(self, root: TxtWord) -> bool:
        """
        The startWithVowelorConsonantDrops method checks for some cases. If the first character of with variable is
        "nsy", and with variable does not equal to one of the Strings; "ylA, ysA, ymHs, yDH, yken", it returns true. If

        Or, if the first character of with variable is 'A, H: or any other vowels, it returns true.

        RETURNS
        -------
        bool
            True if it starts with vowel or consonant drops, false otherwise.
        """
        if (root.isNominal() or root.isAdjective()) and root.nounSoftenDuringSuffixation() and \
                (self.__with == "Hm" or self.__with == "nDAn" or self.__with == "ncA" or self.__with == "nDA"
                 or self.__with == "yA" or self.__with == "yHm" or self.__with == "yHz" or self.__with == "yH"
                 or self.__with == "nH" or self.__with == "nA" or self.__with == "nHn" or self.__with == "H"
                 or self.__with == "sH" or self.__with == "Hn" or self.__with == "HnHz" or self.__with == "HmHz"):
            return True
        if root.isVerb() and root.verbSoftenDuringSuffixation() and \
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

    def makeTransition(self, root: TxtWord, stem: str, startState: State) -> str:
        rootWord = root.getName() == stem or (root.getName() + "'") == stem
        formation = stem
        i = 0
        if self.__with == "0":
            return stem
        if (stem == "bu" or stem == "şu" or stem == "o") and rootWord and self.__with == "ylA":
            return stem + "nunla"
        if self.__with == "yA":
            if stem == "ben":
                return "bana"
            if stem == "sen":
                return "sana"
        self.__formationToCheck = stem
        if rootWord and self.__withFirstChar() == "y" and root.vowelEChangesToIDuringYSuffixation() \
                and (self.__with[1] != "H" or root.getName() == "ye"):
            formation = stem[:len(stem) - 1] + "i"
            self.__formationToCheck = formation
        else:
            if rootWord and (self.__with == "Hl" or self.__with == "Hn") and root.lastIdropsDuringPassiveSuffixation():
                formation = stem[:len(stem) - 2] + stem[len(stem) - 1]
                self.__formationToCheck = stem
            else:
                if rootWord and root.showsSuRegularities() and self.__startWithVowelorConsonantDrops() and \
                        not self.__with.startswith("y"):
                    formation = stem + 'y'
                    self.__formationToCheck = formation
                else:
                    if rootWord and root.duplicatesDuringSuffixation() and not startState.getName().startswith(
                                    "VerbalRoot") and TurkishLanguage.isConsonantDrop(self.__with[0]):
                        if self.softenDuringSuffixation(root):
                            if Word.lastPhoneme(stem) == "p":
                                formation = stem[:len(stem) - 1] + "bb"
                            elif Word.lastPhoneme(stem) == "t":
                                formation = stem[:len(stem) - 1] + "dd"
                        else:
                            formation = stem + stem[len(stem) - 1]
                        self.__formationToCheck = formation
                    else:
                        if rootWord and root.lastIdropsDuringSuffixation() and \
                                not startState.getName().startswith(
                                    "VerbalRoot") and not startState.getName().startswith("ProperRoot") \
                                and self.__startWithVowelorConsonantDrops():
                            if self.softenDuringSuffixation(root):
                                if Word.lastPhoneme(stem) == "p":
                                    formation = stem[:len(stem) - 2] + 'b'
                                elif Word.lastPhoneme(stem) == "t":
                                    formation = stem[:len(stem) - 2] + 'd'
                                elif Word.lastPhoneme(stem) == "ç":
                                    formation = stem[:len(stem) - 2] + 'c'
                            else:
                                formation = stem[:len(stem) - 2] + stem[len(stem) - 1]
                            self.__formationToCheck = stem
                        else:
                            if Word.lastPhoneme(stem) == "p":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'b'
                            elif Word.lastPhoneme(stem) == "t":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'd'
                            elif Word.lastPhoneme(stem) == "ç":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'c'
                            elif Word.lastPhoneme(stem) == "g":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'ğ'
                            elif Word.lastPhoneme(stem) == "k":
                                if self.__startWithVowelorConsonantDrops() and rootWord and root.endingKChangesIntoG() \
                                        and (not root.isProperNoun() or startState.__str__() != "ProperRoot"):
                                    formation = stem[:len(stem) - 1] + 'g'
                                else:
                                    if self.__startWithVowelorConsonantDrops() and (not rootWord or (
                                            self.softenDuringSuffixation(root) and (
                                            not root.isProperNoun() or startState.__str__() != "ProperRoot"))):
                                        formation = stem[:len(stem) - 1] + 'ğ'
                            self.__formationToCheck = formation
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
                    Word.lastPhoneme(stem))) or (rootWord and root.consonantSMayInsertedDuringPossesiveSuffixation()):
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
                formation = MorphotacticEngine.resolveD(root, formation, self.__formationToCheck)
            elif self.__with[i] == "A":
                formation = MorphotacticEngine.resolveA(root, formation, rootWord, self.__formationToCheck)
            elif self.__with[i] == "H":
                if self.__with[0] != "'":
                    formation = MorphotacticEngine.resolveH(root, formation, i == 0, self.__with.startswith("Hyor"), rootWord, self.__formationToCheck)
                else:
                    formation = MorphotacticEngine.resolveH(root, formation, i == 1, False, rootWord, self.__formationToCheck)
            elif self.__with[i] == "C":
                formation = MorphotacticEngine.resolveC(formation, self.__formationToCheck)
            elif self.__with[i] == "S":
                formation = MorphotacticEngine.resolveS(formation)
            elif self.__with[i] == "Ş":
                formation = MorphotacticEngine.resolveSh(formation)
            else:
                if i == len(self.__with) - 1 and self.__with[i] == "s":
                    formation += "ş"
                else:
                    formation += self.__with[i]
            self.__formationToCheck = formation
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
        return self.__withName
