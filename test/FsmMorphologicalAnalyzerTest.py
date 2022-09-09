import unittest

from Corpus.Sentence import Sentence
from Dictionary.TxtWord import TxtWord

from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalAnalysis.State import State
from MorphologicalAnalysis.Transition import Transition


class FsmMorphologicalAnalyzerTest(unittest.TestCase):

    fsm : FsmMorphologicalAnalyzer

    def setUp(self) -> None:
        self.fsm = FsmMorphologicalAnalyzer()

    def test_generateAllParses(self):
        testWords = ["kalp", "göç", "açıkla", "yıldönümü",
                     "resim", "hal", "emlak", "git",
                     "kavur", "ye", "yemek", "ak",
                     "sıska", "yıka", "bul", "cevapla",
                     "coş", "böl", "del", "giy",
                     "kaydol", "anla", "çök", "çık",
                     "doldur", "azal", "göster", "aksa", "cenk"]
        for testWord in testWords:
            word = self.fsm.getDictionary().getWord(testWord)
            if isinstance(word, TxtWord):
                parsesExpected = []
                file = open("../parses/" + word.getName() + ".txt", 'r')
                lines = file.readlines()
                for line in lines:
                    parsesExpected.append(line.split()[1].strip())
                parsesGenerated = self.fsm.generateAllParses(word, len(word.getName()) + 5)
                for parseGenerated in parsesGenerated:
                    print(parseGenerated.getSurfaceForm() + " " + parseGenerated.__str__())
                self.assertTrue(len(parsesExpected), len(parsesGenerated))
                for parseGenerated in parsesGenerated:
                    self.assertTrue(parseGenerated.__str__() in parsesExpected)

    def test_morphologicalAnalysisDataTimeNumber(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("3/4").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("3\\/4").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("4/2/1973").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("14/2/1993").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("14/12/1933").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("6/12/1903").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("%34.5").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("%3").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("%56").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("2:3").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("12:3").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("4:23").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("11:56").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("1:2:3").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("3:12:3").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("5:4:23").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("7:11:56").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("12:2:3").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("10:12:3").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("11:4:23").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("22:11:56").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("45").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("34.23").size() != 0)

    def test_morphologicalAnalysisProperNoun(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isProperNoun():
                    self.assertTrue(self.fsm.morphologicalAnalysis(word.getName().replace("i", "İ").upper()).size() != 0)

    def test_morphologicalAnalysisNounSoftenDuringSuffixation(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isNominal() and word.nounSoftenDuringSuffixation():
                    transitionState = State("Possessive", False, False)
                    startState = State("NominalRoot", True, False)
                    transition = Transition("yH", transitionState, "ACC")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisVowelAChangesToIDuringYSuffixation(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isVerb() and word.vowelAChangesToIDuringYSuffixation():
                    transitionState = State("VerbalStem", False, False)
                    startState = State("VerbalRoot", True, False)
                    transition = Transition("Hyor", transitionState, "PROG1")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisIsPortmanteau(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isNominal() and word.isPortmanteau() and not word.isPlural() and \
                        not word.isPortmanteauFacedVowelEllipsis():
                    transitionState = State("CompoundNounRoot", True, False)
                    startState = State("CompoundNounRoot", True, False)
                    transition = Transition("lArH", transitionState, "A3PL+P3PL")
                    exceptLast2 = word.getName()[:len(word.getName()) - 2]
                    exceptLast = word.getName()[:len(word.getName()) - 1]
                    if word.isPortmanteauFacedSoftening():
                        if word.getName()[len(word.getName()) - 2] == "b":
                            rootForm = exceptLast2 + 'p'
                        elif word.getName()[len(word.getName()) - 2] == "c":
                            rootForm = exceptLast2 + 'ç'
                        elif word.getName()[len(word.getName()) - 2] == "d":
                            rootForm = exceptLast2 + 't'
                        elif word.getName()[len(word.getName()) - 2] == "ğ":
                            rootForm = exceptLast2 + 'k'
                        else:
                            rootForm = exceptLast
                    else:
                        if word.isPortmanteauEndingWithSI():
                            rootForm = exceptLast2
                        else:
                            rootForm = exceptLast
                    surfaceForm = transition.makeTransition(word, rootForm, startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisNotObeysVowelHarmonyDuringAgglutination(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isNominal() and word.notObeysVowelHarmonyDuringAgglutination():
                    transitionState = State("Possessive", False, False)
                    startState = State("NominalRoot", True, False)
                    transition = Transition("yH", transitionState, "ACC")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisLastIdropsDuringSuffixation(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isNominal() and word.lastIdropsDuringSuffixation():
                    transitionState = State("Possessive", False, False)
                    startState = State("NominalRoot", True, False)
                    transition = Transition("yH", transitionState, "ACC")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisVerbSoftenDuringSuffixation(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isVerb() and word.verbSoftenDuringSuffixation():
                    transitionState = State("VerbalStem", False, False)
                    startState = State("VerbalRoot", True, False)
                    transition = Transition("Hyor", transitionState, "PROG1")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisDuplicatesDuringSuffixation(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isNominal() and word.duplicatesDuringSuffixation():
                    transitionState = State("Possessive", False, False)
                    startState = State("NominalRoot", True, False)
                    transition = Transition("yH", transitionState, "ACC")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisEndingKChangesIntoG(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isNominal() and word.endingKChangesIntoG():
                    transitionState = State("Possessive", False, False)
                    startState = State("NominalRoot", True, False)
                    transition = Transition("yH", transitionState, "ACC")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_morphologicalAnalysisLastIdropsDuringPassiveSuffixation(self):
        dictionary = self.fsm.getDictionary()
        for i in range(dictionary.size()):
            word = dictionary.getWordWithIndex(i)
            if isinstance(word, TxtWord):
                if word.isVerb() and word.lastIdropsDuringPassiveSuffixation():
                    transitionState = State("VerbalStem", False, False)
                    startState = State("VerbalRoot", True, False)
                    transition = Transition("Hl", transitionState, "^DB+VERB+PASS")
                    surfaceForm = transition.makeTransition(word, word.getName(), startState)
                    self.assertTrue(self.fsm.morphologicalAnalysis(surfaceForm).size() != 0)

    def test_replaceWord(self):
        self.assertEqual("Şvesterine söyle kazağı güzelmiş", self.fsm.replaceWord(Sentence("Hemşirene söyle kazağı güzelmiş"), "hemşire", "şvester").__str__())
        self.assertEqual("Burada çok abartma var", self.fsm.replaceWord(Sentence("Burada çok mübalağa var"), "mübalağa", "abartma").__str__())
        self.assertEqual("Bu bina çok kötü şekilsizleştirildi", self.fsm.replaceWord(Sentence("Bu bina çok kötü biçimsizleştirildi"), "biçimsizleş", "şekilsizleş").__str__())
        self.assertEqual("Abim geçen yıl ölmüştü gibi", self.fsm.replaceWord(Sentence("Abim geçen yıl son yolculuğa çıkmıştı gibi"), "son yolculuğa çık", "öl").__str__())
        self.assertEqual("Hemşirenle evlendim", self.fsm.replaceWord(Sentence("Kız kardeşinle evlendim"), "kız kardeş", "hemşire").__str__())
        self.assertEqual("Dün yaptığı güreş maçında yenildi", self.fsm.replaceWord(Sentence("Dün yaptığı güreş maçında mağlup oldu"), "mağlup ol", "yenil").__str__())
        self.assertEqual("Abim geçen yıl son yolculuğa çıkmıştı gibi", self.fsm.replaceWord(Sentence("Abim geçen yıl ölmüştü gibi"), "öl", "son yolculuğa çık").__str__())
        self.assertEqual("Kız kardeşinle evlendim", self.fsm.replaceWord(Sentence("Hemşirenle evlendim"), "hemşire", "kız kardeş").__str__())
        self.assertEqual("Dün yaptığı güreş maçında mağlup oldu", self.fsm.replaceWord(Sentence("Dün yaptığı güreş maçında yenildi"), "yenil", "mağlup ol").__str__())
        self.assertEqual("Dün yaptığı güreş maçında alt oldu sanki", self.fsm.replaceWord(Sentence("Dün yaptığı güreş maçında mağlup oldu sanki"), "mağlup ol", "alt ol").__str__())
        self.assertEqual("Yemin billah vermişlerdi vazoyu kırmadığına", self.fsm.replaceWord(Sentence("Yemin etmişlerdi vazoyu kırmadığına"), "yemin et", "yemin billah ver").__str__())
        self.assertEqual("Yemin etmişlerdi vazoyu kırmadığına", self.fsm.replaceWord(Sentence("Yemin billah vermişlerdi vazoyu kırmadığına"), "yemin billah ver", "yemin et").__str__())


if __name__ == '__main__':
    unittest.main()
