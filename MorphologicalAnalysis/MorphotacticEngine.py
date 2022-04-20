from Dictionary.TxtWord import TxtWord
from Dictionary.Word import Word
from Language.TurkishLanguage import TurkishLanguage


class MorphotacticEngine:

    @staticmethod
    def resolveD(root: TxtWord, formation: str, formationToCheck: str) -> str:
        if root.isAbbreviation():
            return formation + 'd'
        if "0" <= Word.lastPhoneme(formationToCheck) <= "9":
            if Word.lastPhoneme(formationToCheck) == "3" or Word.lastPhoneme(formationToCheck) == "4"\
                    or Word.lastPhoneme(formationToCheck) == "5":
                return formation + 't'
            elif Word.lastPhoneme(formationToCheck) == "0":
                if root.getName().endswith("40") or root.getName().endswith("60") or root.getName().endswith("70"):
                    return formation + 't'
                else:
                    return formation + 'd'
            else:
                return formation + 'd'
        else:
            if TurkishLanguage.isSertSessiz(Word.lastPhoneme(formationToCheck)):
                return formation + 't'
            else:
                return formation + 'd'

    @staticmethod
    def resolveA(root: TxtWord, formation: str, rootWord: bool, formationToCheck: str):
        if root.isAbbreviation():
            return formation + 'e'
        if "0" <= Word.lastVowel(formationToCheck) <= "9":
            if Word.lastVowel(formationToCheck) == "6" or Word.lastVowel(formationToCheck) == "9":
                return formation + 'a'
            elif Word.lastVowel(formationToCheck) == "0":
                if root.getName().endswith("10") or root.getName().endswith("30") or root.getName().endswith("40") \
                        or root.getName().endswith("60") or root.getName().endswith("90"):
                    return formation + 'a'
                else:
                    return formation + 'e'
            else:
                return formation + 'e'
        if TurkishLanguage.isBackVowel(Word.lastVowel(formationToCheck)):
            if root.notObeysVowelHarmonyDuringAgglutination() and rootWord:
                return formation + 'e'
            else:
                return formation + 'a'
        if TurkishLanguage.isFrontVowel(Word.lastVowel(formationToCheck)):
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

    @staticmethod
    def resolveH(root: TxtWord, formation: str, beginningOfSuffix: bool, specialCaseTenseSuffix: bool,
                   rootWord: bool, formationToCheck: str):
        if root.isAbbreviation():
            return formation + 'i'
        if beginningOfSuffix and TurkishLanguage.isVowel(Word.lastPhoneme(formationToCheck)) and \
                not specialCaseTenseSuffix:
            return formation
        if specialCaseTenseSuffix:
            if rootWord:
                if root.vowelAChangesToIDuringYSuffixation():
                    if TurkishLanguage.isFrontRoundedVowel(Word.beforeLastVowel(formationToCheck)):
                        return formation[:len(formation) - 1] + 'ü'
                    if TurkishLanguage.isFrontUnroundedVowel(Word.beforeLastVowel(formationToCheck)):
                        return formation[:len(formation) - 1] + 'i'
                    if TurkishLanguage.isBackRoundedVowel(Word.beforeLastVowel(formationToCheck)):
                        return formation[:len(formation) - 1] + 'u'
                    if TurkishLanguage.isBackUnroundedVowel(Word.beforeLastVowel(formationToCheck)):
                        return formation[:len(formation) - 1] + 'ı'
            if TurkishLanguage.isVowel(Word.lastPhoneme(formationToCheck)):
                if TurkishLanguage.isFrontRoundedVowel(Word.beforeLastVowel(formationToCheck)):
                    return formation[:len(formation) - 1] + 'ü'
                if TurkishLanguage.isFrontUnroundedVowel(Word.beforeLastVowel(formationToCheck)):
                    return formation[:len(formation) - 1] + 'i'
                if TurkishLanguage.isBackRoundedVowel(Word.beforeLastVowel(formationToCheck)):
                    return formation[:len(formation) - 1] + 'u'
                if TurkishLanguage.isBackUnroundedVowel(Word.beforeLastVowel(formationToCheck)):
                    return formation[:len(formation) - 1] + 'ı'
        if TurkishLanguage.isFrontRoundedVowel(Word.lastVowel(formationToCheck)) or \
                (TurkishLanguage.isBackRoundedVowel(Word.lastVowel(formationToCheck))
                 and root.notObeysVowelHarmonyDuringAgglutination()):
            return formation + 'ü'
        if TurkishLanguage.isFrontUnroundedVowel(Word.lastVowel(formationToCheck)) or \
                (Word.lastVowel(formationToCheck) == 'a' and root.notObeysVowelHarmonyDuringAgglutination()):
            return formation + 'i'
        if TurkishLanguage.isBackRoundedVowel(Word.lastVowel(formationToCheck)):
            return formation + 'u'
        if TurkishLanguage.isBackUnroundedVowel(Word.lastVowel(formationToCheck)):
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

    @staticmethod
    def resolveC(formation: str, formationToCheck: str) -> str:
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
        if TurkishLanguage.isSertSessiz(Word.lastPhoneme(formationToCheck)):
            return formation + 'ç'
        else:
            return formation + 'c'

    @staticmethod
    def resolveS(formation: str) -> str:
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

    @staticmethod
    def resolveSh(formation: str) -> str:
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
