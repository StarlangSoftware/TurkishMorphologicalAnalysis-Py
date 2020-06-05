from Dictionary.TxtWord import TxtWord
from Language.TurkishLanguage import TurkishLanguage

from MorphologicalAnalysis.FsmParse import FsmParse
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
        if self.__with == "dHr":
            if self.__toState.getName() == "Adverb":
                return True
            else:
                return root.takesSuffixDIRAsFactitive()
        if self.__with == "Hr" and (
                self.__toState.getName() == "AdjectiveRoot(VERB)" or self.__toState.getName() == "OtherTense" or
                self.__toState.getName() == "OtherTense2"):
            return root.takesSuffixIRAsAorist()
        return True

    def __beforeLastVowel(self, stem: str) -> str:
        """
        The beforeLastVowel method takes a str stem as an input. It loops through the given stem and returns
        the second last vowel.

        PARAMETERS
        ----------
        stem : str
            String input.

        RETURNS
        -------
        str
            Vowel before the last vowel.
        """
        last = "0"
        before = 1
        for i in range(len(stem) - 1, -1, -1):
            if TurkishLanguage.isVowel(stem[i]):
                if before == 1:
                    last = stem[i]
                    before = before - 1
                    continue
                return stem[i]
        return last

    def __lastVowel(self, stem: str) -> str:
        """
        The lastVowel method takes a str stem as an input. It loops through the given stem and returns
        the last vowel.

        PARAMETERS
        ----------
        stem : str
            String input.

        RETURNS
        -------
        str
            The last vowel.
        """
        for i in range(len(stem) - 1, - 1, -1):
            if TurkishLanguage.isVowel(stem[i]):
                return stem[i]
        for i in range(len(stem) - 1, -1, -1):
            if "0" <= stem[i] <= "9":
                return stem[i]
        return "0"

    def __lastPhoneme(self, stem: str) -> str:
        """
        The lastPhoneme method takes a str stem as an input. It then returns the last phoneme of the given stem.

        PARAMETERS
        ----------
        stem : str
            String input.

        RETURNS
        -------
        str
            The last phoneme.
        """
        if len(stem) == 0:
            return " "
        if stem[len(stem) - 1] != "'":
            return stem[len(stem) - 1]
        else:
            return stem[len(stem) - 2]

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
        self.__formationToCheck = stem
        if rootWord and self.__withFirstChar() == "y" and root.vowelEChangesToIDuringYSuffixation() \
                and self.__with[1] != "H":
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
                    if rootWord and root.duplicatesDuringSuffixation() and TurkishLanguage.isConsonantDrop(
                            self.__with[0]):
                        if self.softenDuringSuffixation(root):
                            if self.__lastPhoneme(stem) == "p":
                                formation = stem[:len(stem) - 1] + "bb"
                            elif self.__lastPhoneme(stem) == "t":
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
                                if self.__lastPhoneme(stem) == "p":
                                    formation = stem[:len(stem) - 2] + 'b'
                                elif self.__lastPhoneme(stem) == "t":
                                    formation = stem[:len(stem) - 2] + 'd'
                                elif self.__lastPhoneme(stem) == "ç":
                                    formation = stem[:len(stem) - 2] + 'c'
                            else:
                                formation = stem[:len(stem) - 2] + stem[len(stem) - 1]
                            self.__formationToCheck = stem
                        else:
                            if self.__lastPhoneme(stem) == "p":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'b'
                            elif self.__lastPhoneme(stem) == "t":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'd'
                            elif self.__lastPhoneme(stem) == "ç":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'c'
                            elif self.__lastPhoneme(stem) == "g":
                                if self.__startWithVowelorConsonantDrops() and rootWord and \
                                        self.softenDuringSuffixation(root):
                                    formation = stem[:len(stem) - 1] + 'ğ'
                            elif self.__lastPhoneme(stem) == "k":
                                if self.__startWithVowelorConsonantDrops() and rootWord and root.endingKChangesIntoG() \
                                        and not root.isProperNoun():
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
                    self.__lastPhoneme(stem))) or (rootWord and root.consonantSMayInsertedDuringPossesiveSuffixation()):
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
                formation = self.__resolveD(root, formation)
            elif self.__with[i] == "A":
                formation = self.__resolveA(root, formation, rootWord)
            elif self.__with[i] == "H":
                if self.__with[0] != "'":
                    formation = self.__resolveH(root, formation, i == 0, self.__with.startswith("Hyor"), rootWord)
                else:
                    formation = self.__resolveH(root, formation, i == 1, False, rootWord)
            elif self.__with[i] == "C":
                formation = self.__resolveC(formation)
            elif self.__with[i] == "S":
                formation = self.__resolveS(formation)
            elif self.__with[i] == "Ş":
                formation = self.__resolveSh(formation)
            else:
                if i == len(self.__with) - 1 and self.__with[i] == "s":
                    formation += "ş"
                else:
                    formation += self.__with[i]
            self.__formationToCheck = formation
            i = i + 1
        return formation

    def __resolveD(self, root: TxtWord, formation: str) -> str:
        if root.isAbbreviation():
            return formation + 'd'
        if "0" <= self.__lastPhoneme(self.__formationToCheck) <= "9":
            if self.__lastPhoneme(self.__formationToCheck) == "3" or self.__lastPhoneme(self.__formationToCheck) == "4"\
                    or self.__lastPhoneme(self.__formationToCheck) == "5":
                return formation + 't'
            elif self.__lastPhoneme(self.__formationToCheck) == "0":
                if root.getName().endswith("40") or root.getName().endswith("60") or root.getName().endswith("70"):
                    return formation + 't'
                else:
                    return formation + 'd'
            else:
                return formation + 'd'
        else:
            if TurkishLanguage.isSertSessiz(self.__lastPhoneme(self.__formationToCheck)):
                return formation + 't'
            else:
                return formation + 'd'

    def __resolveA(self, root: TxtWord, formation: str, rootWord: bool):
        if root.isAbbreviation():
            return formation + 'e'
        if "0" <= self.__lastVowel(self.__formationToCheck) <= "9":
            if self.__lastVowel(self.__formationToCheck) == "6" or self.__lastVowel(self.__formationToCheck) == "9":
                return formation + 'a'
            elif self.__lastVowel(self.__formationToCheck) == "0":
                if root.getName().endswith("10") or root.getName().endswith("30") or root.getName().endswith("40") \
                        or root.getName().endswith("60") or root.getName().endswith("90"):
                    return formation + 'a'
                else:
                    return formation + 'e'
            else:
                return formation + 'e'
        if TurkishLanguage.isBackVowel(self.__lastVowel(self.__formationToCheck)):
            if root.notObeysVowelHarmonyDuringAgglutination() and rootWord:
                return formation + 'e'
            else:
                return formation + 'a'
        if TurkishLanguage.isFrontVowel(self.__lastVowel(self.__formationToCheck)):
            if root.notObeysVowelHarmonyDuringAgglutination() and rootWord:
                return formation + 'a'
            else:
                return formation + 'e'
        if root.isNumeral() or root.isFraction() or root.isReal():
            if root.getName().endswith("6") or root.getName().endswith("9") or root.getName().endswith("10") or \
                    root.getName().endswith("30") or root.getName().endswith("40") or root.getName().endswith("60") \
                    or root.getName().endswith("90"):
                return formation + 'a'
            else:
                return formation + 'e'
        return formation

    def __resolveH(self, root: TxtWord, formation: str, beginningOfSuffix: bool, specialCaseTenseSuffix: bool,
                   rootWord: bool):
        if root.isAbbreviation():
            return formation + 'i'
        if beginningOfSuffix and TurkishLanguage.isVowel(self.__lastPhoneme(self.__formationToCheck)) and \
                not specialCaseTenseSuffix:
            return formation
        if specialCaseTenseSuffix:
            if rootWord:
                if root.vowelAChangesToIDuringYSuffixation():
                    if TurkishLanguage.isFrontRoundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                        return formation[:len(formation) - 1] + 'ü'
                    if TurkishLanguage.isFrontUnroundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                        return formation[:len(formation) - 1] + 'i'
                    if TurkishLanguage.isBackRoundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                        return formation[:len(formation) - 1] + 'u'
                    if TurkishLanguage.isBackUnroundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                        return formation[:len(formation) - 1] + 'ı'
            if TurkishLanguage.isVowel(self.__lastPhoneme(self.__formationToCheck)):
                if TurkishLanguage.isFrontRoundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                    return formation[:len(formation) - 1] + 'ü'
                if TurkishLanguage.isFrontUnroundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                    return formation[:len(formation) - 1] + 'i'
                if TurkishLanguage.isBackRoundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                    return formation[:len(formation) - 1] + 'u'
                if TurkishLanguage.isBackUnroundedVowel(self.__beforeLastVowel(self.__formationToCheck)):
                    return formation[:len(formation) - 1] + 'ı'
        if TurkishLanguage.isFrontRoundedVowel(self.__lastVowel(self.__formationToCheck)) or \
                (TurkishLanguage.isBackRoundedVowel(self.__lastVowel(self.__formationToCheck))
                 and root.notObeysVowelHarmonyDuringAgglutination()):
            return formation + 'ü'
        if TurkishLanguage.isFrontUnroundedVowel(self.__lastVowel(self.__formationToCheck)) or \
                (self.__lastVowel(self.__formationToCheck) == 'a' and root.notObeysVowelHarmonyDuringAgglutination()):
            return formation + 'i'
        if TurkishLanguage.isBackRoundedVowel(self.__lastVowel(self.__formationToCheck)):
            return formation + 'u'
        if TurkishLanguage.isBackUnroundedVowel(self.__lastVowel(self.__formationToCheck)):
            return formation + 'ı'
        if root.isNumeral() or root.isFraction() or root.isReal():
            if root.getName().endswith("6") or root.getName().endswith("40") or root.getName().endswith("60") \
                    or root.getName().endswith("90"):
                return formation + 'ı'
            else:
                if root.getName().endswith("3") or root.getName().endswith("4") or root.getName().endswith("00"):
                    return formation + 'ü'
                else:
                    if root.getName().endswith("9") or root.getName().endswith("10") or root.getName().endswith("30"):
                        return formation + 'u'
                    else:
                        return formation + 'i'
        return formation

    def __resolveC(self, formation: str) -> str:
        """
        The resolveC method takes a str formation as an input. If the last phoneme is on of the "çfhkpsşt", it
        concatenates given formation with 'ç', if not it concatenates given formation with 'c'.

        PARAMETERS
        ----------
        formation : str
            String input.

        RETURNS
        -------
        str
            Resolved String.
        """
        if TurkishLanguage.isSertSessiz(self.__lastPhoneme(self.__formationToCheck)):
            return formation + 'ç'
        else:
            return formation + 'c'

    def __resolveS(self, formation: str) -> str:
        """
        The resolveS method takes a str formation as an input. It then concatenates given formation with 's'.

        PARAMETERS
        ----------
        formation : str
            String input.

        RETURNS
        -------
        str
            Resolved String.
        """
        return formation + 's'

    def __resolveSh(self, formation: str) -> str:
        """
        The resolveSh method takes a str formation as an input. If the last character is a vowel, it concatenates
        given formation with ş, if the last character is not a vowel, and not 't' it directly returns given formation,
        but if it is equal to 't', it transforms it to 'd'.

        PARAMETERS
        ----------
        formation : str
            String input.

        RETURNS
        -------
        str
            Resolved String.
        """
        if TurkishLanguage.isVowel(formation[len(formation) - 1]):
            return formation + 'ş'
        else:
            if formation[len(formation) - 1] != 't':
                return formation
            else:
                return formation[len(formation) - 1] + 'd'

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
