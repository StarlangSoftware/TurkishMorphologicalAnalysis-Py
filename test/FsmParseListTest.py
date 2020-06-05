import unittest

from Dictionary.Word import Word

from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalAnalysis.FsmParseList import FsmParseList


class FsmParseListTest(unittest.TestCase):

    parse1 : FsmParseList
    parse2 : FsmParseList
    parse3 : FsmParseList
    parse4 : FsmParseList
    parse5 : FsmParseList
    parse6 : FsmParseList
    parse7 : FsmParseList
    parse8 : FsmParseList
    parse9 : FsmParseList

    def setUp(self) -> None:
        fsm = FsmMorphologicalAnalyzer("../turkish_dictionary.txt", "../turkish_misspellings.txt", "../turkish_finite_state_machine.xml")
        self.parse1 = fsm.morphologicalAnalysis("açılır")
        self.parse2 = fsm.morphologicalAnalysis("koparılarak")
        self.parse3 = fsm.morphologicalAnalysis("toplama")
        self.parse4 = fsm.morphologicalAnalysis("değerlendirmede")
        self.parse5 = fsm.morphologicalAnalysis("soruşturmasının")
        self.parse6 = fsm.morphologicalAnalysis("karşılaştırmalı")
        self.parse7 = fsm.morphologicalAnalysis("esaslarını")
        self.parse8 = fsm.morphologicalAnalysis("güçleriyle")
        self.parse9 = fsm.morphologicalAnalysis("bulmayacakları")

    def test_Size(self):
         self.assertEqual(2, self.parse1.size())
         self.assertEqual(2, self.parse2.size())
         self.assertEqual(6, self.parse3.size())
         self.assertEqual(4, self.parse4.size())
         self.assertEqual(5, self.parse5.size())
         self.assertEqual(12, self.parse6.size())
         self.assertEqual(8, self.parse7.size())
         self.assertEqual(6, self.parse8.size())
         self.assertEqual(5, self.parse9.size())

    def test_RootWords(self):
         self.assertEqual("aç", self.parse1.rootWords())
         self.assertEqual("kop$kopar", self.parse2.rootWords())
         self.assertEqual("topla$toplam$toplama", self.parse3.rootWords())
         self.assertEqual("değer$değerlen$değerlendir$değerlendirme", self.parse4.rootWords())
         self.assertEqual("sor$soru$soruş$soruştur$soruşturma", self.parse5.rootWords())
         self.assertEqual("karşı$karşıla$karşılaş$karşılaştır$karşılaştırma$karşılaştırmalı", self.parse6.rootWords())
         self.assertEqual("esas", self.parse7.rootWords())
         self.assertEqual("güç", self.parse8.rootWords())
         self.assertEqual("bul", self.parse9.rootWords())

    def test_GetParseWithLongestRootWord(self):
         self.assertEqual(Word("kopar"), self.parse2.getParseWithLongestRootWord().root)
         self.assertEqual(Word("toplama"), self.parse3.getParseWithLongestRootWord().root)
         self.assertEqual(Word("değerlendirme"), self.parse4.getParseWithLongestRootWord().root)
         self.assertEqual(Word("soruşturma"), self.parse5.getParseWithLongestRootWord().root)
         self.assertEqual(Word("karşılaştırmalı"), self.parse6.getParseWithLongestRootWord().root)

    def test_ReduceToParsesWithSameRootAndPos(self):
        self.parse2.reduceToParsesWithSameRootAndPos(Word("kop+VERB"))
        self.assertEqual(1, self.parse2.size())
        self.parse3.reduceToParsesWithSameRootAndPos(Word("topla+VERB"))
        self.assertEqual(2, self.parse3.size())
        self.parse6.reduceToParsesWithSameRootAndPos(Word("karşıla+VERB"))
        self.assertEqual(2, self.parse6.size())

    def test_ReduceToParsesWithSameRoot(self):
        self.parse2.reduceToParsesWithSameRoot("kop")
        self.assertEqual(1, self.parse2.size())
        self.parse3.reduceToParsesWithSameRoot("topla")
        self.assertEqual(3, self.parse3.size())
        self.parse6.reduceToParsesWithSameRoot("karşı")
        self.assertEqual(4, self.parse6.size())
        self.parse7.reduceToParsesWithSameRoot("esas")
        self.assertEqual(8, self.parse7.size())
        self.parse8.reduceToParsesWithSameRoot("güç")
        self.assertEqual(6, self.parse8.size())

    def test_ConstructParseListForDifferentRootWithPos(self):
         self.assertEqual(1, len(self.parse1.constructParseListForDifferentRootWithPos()))
         self.assertEqual(2, len(self.parse2.constructParseListForDifferentRootWithPos()))
         self.assertEqual(5, len(self.parse3.constructParseListForDifferentRootWithPos()))
         self.assertEqual(4, len(self.parse4.constructParseListForDifferentRootWithPos()))
         self.assertEqual(5, len(self.parse5.constructParseListForDifferentRootWithPos()))
         self.assertEqual(7, len(self.parse6.constructParseListForDifferentRootWithPos()))
         self.assertEqual(2, len(self.parse7.constructParseListForDifferentRootWithPos()))
         self.assertEqual(2, len(self.parse8.constructParseListForDifferentRootWithPos()))
         self.assertEqual(1, len(self.parse9.constructParseListForDifferentRootWithPos()))


if __name__ == '__main__':
    unittest.main()
