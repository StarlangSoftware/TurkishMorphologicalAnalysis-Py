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

    """
    Constructor of Transition class which takes a State, and three str as input. Then it
    initializes toState, with, withName and toPos variables with given inputs.

    PARAMETERS
    ----------
    with : str    
        String input.
    toState : State 
        State input.
    withName : str
        String input.
    toPos : str   
        String input.
    """

    def __init__(self, _with: str, toState=None, withName=None, toPos=None):
        self.__with = _with
        self.__toState = toState
        self.__withName = withName
        self.__toPos = toPos

    """
    Getter for the toState variable.

    RETURNS
    -------
    State
        toState variable.
    """

    def toState(self) -> State:
        return self.__toState

    """
    Getter for the toPos variable.

    RETURNS
    -------
    str
        toPos variable.
    """

    def toPos(self) -> str:
        return self.__toPos

    """
    The transitionPossibleForString method takes two str as inputs; currentSurfaceForm and realSurfaceForm. If the
    length of the given currentSurfaceForm is greater than the given realSurfaceForm, it directly returns true. If not,
    it takes a substring from given realSurfaceForm with the size of currentSurfaceForm. Then checks for the characters 
    of with variable.

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

    def transitionPossibleForString(self, currentSurfaceForm: str, realSurfaceForm: str) -> bool:
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

    """
    The transitionPossibleForParse method takes a FsmParse currentFsmParse as an input. It then checks some special cases;

    PARAMETERS
    ----------
    currentFsmParse : FsmParse
        Parse to be checked
        
    RETURNS
    -------
    bool
        True if transition is possible False otherwise
    """

    def transitionPossibleForParse(self, currentFsmParse: FsmParse) -> bool:
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
                self.__toState.getName() == "AdjectiveRoot(VERB)" or self.__toState.getName() == "OtherTense" or self.__toState.getName() == "OtherTense2"):
            return root.takesSuffixIRAsAorist()
        return True

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

    def beforeLastVowel(self, stem: str) -> str:
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

    def lastVowel(self, stem: str) -> str:
        for i in range(len(stem) - 1, - 1, -1):
            if TurkishLanguage.isVowel(stem[i]):
                return stem[i]
        for i in range(len(stem) - 1, -1, -1):
            if "0" <= stem[i] <= "9":
                return stem[i]
        return "0"

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

    def lastPhoneme(self, stem: str) -> str:
        if len(stem) == 0:
            return " "
        if stem[len(stem) - 1] != "'":
            return stem[len(stem) - 1]
        else:
            return stem[len(stem) - 2]

    """
    The withFirstChar method returns the first character of the with variable.

    RETURNS
    -------
    str
        The first character of the with variable.
    """

    def withFirstChar(self) -> str:
        if len(self.__with) == 0:
            return "$"
        if self.__with[0] != "'":
            return self.__with[0]
        elif len(self.__with) == 1:
            return self.__with[0]
        else:
            return self.__with[1]

    """
    The startWithVowelorConsonantDrops method checks for some cases. If the first character of with variable is "nsy",
    and with variable does not equal to one of the Strings; "ylA, ysA, ymHs, yDH, yken", it returns true. If

    Or, if the first character of with variable is 'A, H: or any other vowels, it returns true.

    RETURNS
    -------
    bool
        True if it starts with vowel or consonant drops, false otherwise.
    """

    def startWithVowelorConsonantDrops(self) -> bool:
        if TurkishLanguage.isConsonantDrop(self.withFirstChar()) and self.__with != "ylA" and self.__with != "ysA" \
                and self.__with != "ymHs" and self.__with != "yDH" and self.__with != "yken":
            return True
        if self.withFirstChar() == "A" or self.withFirstChar() == "H" or TurkishLanguage.isVowel(self.withFirstChar()):
            return True
        return False

    """
    The softenDuringSuffixation method takes a TxtWord root as an input. It checks two cases; first case returns
    true if the given root is nominal or adjective and has one of the flags "IS_SD, IS_B_SD, IS_SDD" and with variable
    equals o one of the Strings "Hm, nDAn, ncA, nDA, yA, yHm, yHz, yH, nH, nA, nHn, H, sH, Hn, HnHz, HmHz".

    And the second case returns true if the given root is verb and has the "F_SD" flag, also with variable starts with
    "Hyor" or equals one of the Strings "yHs, yAn, yA, yAcAk, yAsH, yHncA, yHp, yAlH, yArAk, yAdur, yHver, yAgel, yAgor,
    yAbil, yAyaz, yAkal, yAkoy, yAmA, yHcH, HCH, Hr, Hs, Hn, yHn", yHnHz, Ar, Hl").

    PARAMETERS
    ----------
    root : TxtWord
        TxtWord input.
        
    RETURNS
    -------
    bool
        True if there is softening during suffixation of the given root, False otherwise.
    """

    def softenDuringSuffixation(self, root: TxtWord) -> bool:
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

    def makeTransitionNoStartState(self, root: TxtWord, stem: str) -> str:
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
        if rootWord and self.withFirstChar() == "y" and root.vowelEChangesToIDuringYSuffixation() \
                and self.__with[1] != "H":
            formation = stem[:len(stem) - 1] + "i"
            self.__formationToCheck = formation
        else:
            if rootWord and (self.__with == "Hl" or self.__with == "Hn") and root.lastIdropsDuringPassiveSuffixation():
                formation = stem[:len(stem) - 2] + stem[len(stem) - 1]
                self.__formationToCheck = stem
            else:
                if rootWord and root.showsSuRegularities() and self.startWithVowelorConsonantDrops() and \
                        not self.__with.startswith("y"):
                    formation = stem + 'y'
                    self.__formationToCheck = formation
                else:
                    if rootWord and root.duplicatesDuringSuffixation() and TurkishLanguage.isConsonantDrop(
                            self.__with[0]):
                        if self.softenDuringSuffixation(root):
                            if self.lastPhoneme(stem) == "p":
                                formation = stem[:len(stem) - 1] + "bb"
                            elif self.lastPhoneme(stem) == "t":
                                formation = stem[:len(stem) - 1] + "dd"
                        else:
                            formation = stem + stem[len(stem) - 1]
                        self.__formationToCheck = formation
                    else:
                        if rootWord and root.lastIdropsDuringSuffixation() and \
                                not startState.getName().startswith(
                                    "VerbalRoot") and not startState.getName().startswith("ProperRoot") \
                                and self.startWithVowelorConsonantDrops():
                            if self.softenDuringSuffixation(root):
                                if self.lastPhoneme(stem) == "p":
                                    formation = stem[:len(stem) - 2] + 'b'
                                elif self.lastPhoneme(stem) == "t":
                                    formation = stem[:len(stem) - 2] + 'd'
                                elif self.lastPhoneme(stem) == "ç":
                                    formation = stem[:len(stem) - 2] + 'c'
                            else:
                                formation = stem[:len(stem) - 2] + stem[len(stem) - 1]
                            self.__formationToCheck = stem
                        else:
                            if self.lastPhoneme(stem) == "p":
                                if self.startWithVowelorConsonantDrops() and rootWord and self.softenDuringSuffixation(
                                        root):
                                    formation = stem[:len(stem) - 1] + 'b'
                            elif self.lastPhoneme(stem) == "t":
                                if self.startWithVowelorConsonantDrops() and rootWord and self.softenDuringSuffixation(
                                        root):
                                    formation = stem[:len(stem) - 1] + 'd'
                            elif self.lastPhoneme(stem) == "ç":
                                if self.startWithVowelorConsonantDrops() and rootWord and self.softenDuringSuffixation(
                                        root):
                                    formation = stem[:len(stem) - 1] + 'c'
                            elif self.lastPhoneme(stem) == "g":
                                if self.startWithVowelorConsonantDrops() and rootWord and self.softenDuringSuffixation(
                                        root):
                                    formation = stem[:len(stem) - 1] + 'ğ'
                            elif self.lastPhoneme(stem) == "k":
                                if self.startWithVowelorConsonantDrops() and rootWord and root.endingKChangesIntoG() \
                                        and not root.isProperNoun():
                                    formation = stem[:len(stem) - 1] + 'g'
                                else:
                                    if self.startWithVowelorConsonantDrops() and (not rootWord or (
                                            self.softenDuringSuffixation(root) and (
                                            not root.isProperNoun() or startState.__str__() != "ProperRoot"))):
                                        formation = stem[:len(stem) - 1] + 'ğ'
                            self.__formationToCheck = formation
        if TurkishLanguage.isConsonantDrop(self.withFirstChar()) and not TurkishLanguage.isVowel(stem[len(stem) - 1]) \
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
            if (TurkishLanguage.isConsonantDrop(self.withFirstChar()) and TurkishLanguage.isConsonant(
                    self.lastPhoneme(stem))) or (rootWord and root.consonantSMayInsertedDuringPossesiveSuffixation()):
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
                formation = self.resolveD(root, formation)
            elif self.__with[i] == "A":
                formation = self.resolveA(root, formation, rootWord)
            elif self.__with[i] == "H":
                if self.__with[0] != "'":
                    formation = self.resolveH(root, formation, i == 0, self.__with.startswith("Hyor"), rootWord)
                else:
                    formation = self.resolveH(root, formation, i == 1, False, rootWord)
            elif self.__with[i] == "C":
                formation = self.resolveC(formation)
            elif self.__with[i] == "S":
                formation = self.resolveS(formation)
            elif self.__with[i] == "Ş":
                formation = self.resolveSh(formation)
            else:
                if i == len(self.__with) - 1 and self.__with[i] == "s":
                    formation += "ş"
                else:
                    formation += self.__with[i]
            self.__formationToCheck = formation
            i = i + 1
        return formation

    def resolveD(self, root: TxtWord, formation: str) -> str:
        if root.isAbbreviation():
            return formation + 'd'
        if "0" <= self.lastPhoneme(self.__formationToCheck) <= "9":
            if self.lastPhoneme(self.__formationToCheck) == "3" or self.lastPhoneme(self.__formationToCheck) == "4" \
                    or self.lastPhoneme(self.__formationToCheck) == "5":
                return formation + 't'
            elif self.lastPhoneme(self.__formationToCheck) == "0":
                if root.getName().endswith("40") or root.getName().endswith("60") or root.getName().endswith("70"):
                    return formation + 't'
                else:
                    return formation + 'd'
            else:
                return formation + 'd'
        else:
            if TurkishLanguage.isSertSessiz(self.lastPhoneme(self.__formationToCheck)):
                return formation + 't'
            else:
                return formation + 'd'

    def resolveA(self, root: TxtWord, formation: str, rootWord: bool):
        if root.isAbbreviation():
            return formation + 'e'
        if "0" <= self.lastVowel(self.__formationToCheck) <= "9":
            if self.lastVowel(self.__formationToCheck) == "6" or self.lastVowel(self.__formationToCheck) == 9:
                return formation + 'a'
            elif self.lastVowel(self.__formationToCheck) == "0":
                if root.getName().endswith("10") or root.getName().endswith("30") or root.getName().endswith("40") \
                        or root.getName().endswith("60") or root.getName().endswith("90"):
                    return formation + 'a'
                else:
                    return formation + 'e'
            else:
                return formation + 'e'
        if TurkishLanguage.isBackVowel(self.lastVowel(self.__formationToCheck)):
            if root.notObeysVowelHarmonyDuringAgglutination() and rootWord:
                return formation + 'e'
            else:
                return formation + 'a'
        if TurkishLanguage.isFrontVowel(self.lastVowel(self.__formationToCheck)):
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

    def resolveH(self, root: TxtWord, formation: str, beginningOfSuffix: bool, specialCaseTenseSuffix: bool, rootWord: bool):
        if root.isAbbreviation():
            return formation + 'i'
        if beginningOfSuffix and TurkishLanguage.isVowel(self.lastPhoneme(self.__formationToCheck)) and not specialCaseTenseSuffix:
            return formation
        if specialCaseTenseSuffix:
            if rootWord:
                if root.vowelAChangesToIDuringYSuffixation():
                    if TurkishLanguage.isFrontRoundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                        return formation[:len(formation) - 1] + 'ü'
                    if TurkishLanguage.isFrontUnroundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                        return formation[:len(formation) - 1] + 'i'
                    if TurkishLanguage.isBackRoundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                        return formation[:len(formation) - 1] + 'u'
                    if TurkishLanguage.isBackUnroundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                        return formation[len(formation) - 1] + 'ı'
            if TurkishLanguage.isVowel(self.lastPhoneme(self.__formationToCheck)):
                if TurkishLanguage.isFrontRoundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                    return formation[len(formation) - 1] + 'ü'
                if TurkishLanguage.isFrontUnroundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                    return formation[len(formation) - 1] + 'i'
                if TurkishLanguage.isBackRoundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                    return formation[len(formation) - 1] + 'u'
                if TurkishLanguage.isBackUnroundedVowel(self.beforeLastVowel(self.__formationToCheck)):
                    return formation[len(formation) - 1] + 'ı'
        if TurkishLanguage.isFrontRoundedVowel(self.lastVowel(self.__formationToCheck)) or \
                (TurkishLanguage.isBackRoundedVowel(self.lastVowel(self.__formationToCheck))
                 and root.notObeysVowelHarmonyDuringAgglutination()):
            return formation + 'ü'
        if TurkishLanguage.isFrontUnroundedVowel(self.lastVowel(self.__formationToCheck)) or \
                (self.lastVowel(self.__formationToCheck) == 'a' and root.notObeysVowelHarmonyDuringAgglutination()):
            return formation + 'i'
        if TurkishLanguage.isBackRoundedVowel(self.lastVowel(self.__formationToCheck)):
            return formation + 'u'
        if TurkishLanguage.isBackUnroundedVowel(self.lastVowel(self.__formationToCheck)):
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
    def resolveC(self, formation: str) -> str:
        if TurkishLanguage.isSertSessiz(self.lastPhoneme(self.__formationToCheck)):
            return formation + 'ç'
        else:
            return formation + 'c'

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
    def resolveS(self, formation: str) -> str:
        return formation + 's'

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
    def resolveSh(self, formation: str) -> str:
        if TurkishLanguage.isVowel(formation[len(formation) - 1]):
            return formation + 'ş'
        else:
            if formation[len(formation) - 1] != 't':
                return formation
            else:
                return formation[len(formation) - 1] + 'd'

    """
    An overridden toString method which returns the with variable.

    RETURNS
    -------
    str
        With variable.
    """
    def __str__(self):
        return self.__with

    """
    The withName method returns the withName variable.

    RETURNS
    -------
    str
        The withName variable.
    """
    def withName(self) -> str:
        return self.__withName
