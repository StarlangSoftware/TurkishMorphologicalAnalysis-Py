import unittest

from MorphologicalAnalysis.MorphologicalParse import MorphologicalParse


class MorphologicalParseTest(unittest.TestCase):

    parse1: MorphologicalParse
    parse2: MorphologicalParse
    parse3: MorphologicalParse
    parse4: MorphologicalParse
    parse5: MorphologicalParse
    parse6: MorphologicalParse
    parse7: MorphologicalParse
    parse8: MorphologicalParse
    parse9: MorphologicalParse

    def setUp(self) -> None:
        self.parse1 = MorphologicalParse("bayan+NOUN+A3SG+PNON+NOM")
        self.parse2 = MorphologicalParse("yaşa+VERB+POS^DB+ADJ+PRESPART")
        self.parse3 = MorphologicalParse("serbest+ADJ")
        self.parse4 = MorphologicalParse("et+VERB^DB+VERB+PASS^DB+VERB+ABLE+NEG+AOR+A3SG")
        self.parse5 = MorphologicalParse("sür+VERB^DB+VERB+CAUS^DB+VERB+PASS+POS^DB+NOUN+INF2+A3SG+P3SG+NOM")
        self.parse6 = MorphologicalParse("değiş+VERB^DB+VERB+CAUS^DB+VERB+PASS+POS^DB+VERB+ABLE+AOR^DB+ADJ+ZERO")
        self.parse7 = MorphologicalParse("iyi+ADJ^DB+VERB+BECOME^DB+VERB+CAUS^DB+VERB+PASS+POS^DB+VERB+ABLE^DB+NOUN+INF2+A3PL+P3PL+ABL")
        self.parse8 = MorphologicalParse("değil+ADJ^DB+VERB+ZERO+PAST+A3SG")
        self.parse9 = MorphologicalParse("hazır+ADJ^DB+VERB+ZERO+PAST+A3SG")

    def test_GetTransitionList(self):
        self.assertEqual("NOUN+A3SG+PNON+NOM", self.parse1.getTransitionList())
        self.assertEqual("VERB+POS+ADJ+PRESPART", self.parse2.getTransitionList())
        self.assertEqual("ADJ", self.parse3.getTransitionList())
        self.assertEqual("VERB+VERB+PASS+VERB+ABLE+NEG+AOR+A3SG", self.parse4.getTransitionList())
        self.assertEqual("VERB+VERB+CAUS+VERB+PASS+POS+NOUN+INF2+A3SG+P3SG+NOM", self.parse5.getTransitionList())
        self.assertEqual("VERB+VERB+CAUS+VERB+PASS+POS+VERB+ABLE+AOR+ADJ+ZERO", self.parse6.getTransitionList())
        self.assertEqual("ADJ+VERB+BECOME+VERB+CAUS+VERB+PASS+POS+VERB+ABLE+NOUN+INF2+A3PL+P3PL+ABL", self.parse7.getTransitionList())
        self.assertEqual("ADJ+VERB+ZERO+PAST+A3SG", self.parse8.getTransitionList())

    def test_GetTag(self):
        self.assertEqual("A3SG", self.parse1.getTag(2))
        self.assertEqual("PRESPART", self.parse2.getTag(4))
        self.assertEqual("serbest", self.parse3.getTag(0))
        self.assertEqual("AOR", self.parse4.getTag(7))
        self.assertEqual("P3SG", self.parse5.getTag(10))
        self.assertEqual("ABLE", self.parse6.getTag(8))
        self.assertEqual("ABL", self.parse7.getTag(15))

    def test_GetTagSize(self):
        self.assertEqual(5, self.parse1.tagSize())
        self.assertEqual(5, self.parse2.tagSize())
        self.assertEqual(2, self.parse3.tagSize())
        self.assertEqual(9, self.parse4.tagSize())
        self.assertEqual(12, self.parse5.tagSize())
        self.assertEqual(12, self.parse6.tagSize())
        self.assertEqual(16, self.parse7.tagSize())
        self.assertEqual(6, self.parse8.tagSize())

    def test_Size(self):
        self.assertEqual(1, self.parse1.size())
        self.assertEqual(2, self.parse2.size())
        self.assertEqual(1, self.parse3.size())
        self.assertEqual(3, self.parse4.size())
        self.assertEqual(4, self.parse5.size())
        self.assertEqual(5, self.parse6.size())
        self.assertEqual(6, self.parse7.size())
        self.assertEqual(2, self.parse8.size())

    def test_GetRootPos(self):
        self.assertEqual("NOUN", self.parse1.getRootPos())
        self.assertEqual("VERB", self.parse2.getRootPos())
        self.assertEqual("ADJ", self.parse3.getRootPos())
        self.assertEqual("VERB", self.parse4.getRootPos())
        self.assertEqual("VERB", self.parse5.getRootPos())
        self.assertEqual("VERB", self.parse6.getRootPos())
        self.assertEqual("ADJ", self.parse7.getRootPos())
        self.assertEqual("ADJ", self.parse8.getRootPos())

    def test_GetPos(self):
        self.assertEqual("NOUN", self.parse1.getPos())
        self.assertEqual("ADJ", self.parse2.getPos())
        self.assertEqual("ADJ", self.parse3.getPos())
        self.assertEqual("VERB", self.parse4.getPos())
        self.assertEqual("NOUN", self.parse5.getPos())
        self.assertEqual("ADJ", self.parse6.getPos())
        self.assertEqual("NOUN", self.parse7.getPos())
        self.assertEqual("VERB", self.parse8.getPos())

    def test_GetWordWithPos(self):
        self.assertEqual("bayan+NOUN", self.parse1.getWordWithPos().getName())
        self.assertEqual("yaşa+VERB", self.parse2.getWordWithPos().getName())
        self.assertEqual("serbest+ADJ", self.parse3.getWordWithPos().getName())
        self.assertEqual("et+VERB", self.parse4.getWordWithPos().getName())
        self.assertEqual("sür+VERB", self.parse5.getWordWithPos().getName())
        self.assertEqual("değiş+VERB", self.parse6.getWordWithPos().getName())
        self.assertEqual("iyi+ADJ", self.parse7.getWordWithPos().getName())
        self.assertEqual("değil+ADJ", self.parse8.getWordWithPos().getName())

    def test_LastIGContainsCase(self):
        self.assertEqual("NOM", self.parse1.lastIGContainsCase())
        self.assertEqual("NULL", self.parse2.lastIGContainsCase())
        self.assertEqual("NULL", self.parse3.lastIGContainsCase())
        self.assertEqual("NULL", self.parse4.lastIGContainsCase())
        self.assertEqual("NOM", self.parse5.lastIGContainsCase())
        self.assertEqual("NULL", self.parse6.lastIGContainsCase())
        self.assertEqual("ABL", self.parse7.lastIGContainsCase())

    def test_LastIGContainsPossessive(self):
        self.assertFalse(self.parse1.lastIGContainsPossessive())
        self.assertFalse(self.parse2.lastIGContainsPossessive())
        self.assertFalse(self.parse3.lastIGContainsPossessive())
        self.assertFalse(self.parse4.lastIGContainsPossessive())
        self.assertTrue(self.parse5.lastIGContainsPossessive())
        self.assertFalse(self.parse6.lastIGContainsPossessive())
        self.assertTrue(self.parse7.lastIGContainsPossessive())

    def test_IsPlural(self):
        self.assertFalse(self.parse1.isPlural())
        self.assertFalse(self.parse2.isPlural())
        self.assertFalse(self.parse3.isPlural())
        self.assertFalse(self.parse4.isPlural())
        self.assertFalse(self.parse5.isPlural())
        self.assertFalse(self.parse6.isPlural())
        self.assertTrue(self.parse7.isPlural())

    def test_IsAuxiliary(self):
        self.assertFalse(self.parse1.isAuxiliary())
        self.assertFalse(self.parse2.isAuxiliary())
        self.assertFalse(self.parse3.isAuxiliary())
        self.assertTrue(self.parse4.isAuxiliary())
        self.assertFalse(self.parse5.isAuxiliary())
        self.assertFalse(self.parse6.isAuxiliary())
        self.assertFalse(self.parse7.isAuxiliary())

    def test_IsNoun(self):
        self.assertTrue(self.parse1.isNoun())
        self.assertTrue(self.parse5.isNoun())
        self.assertTrue(self.parse7.isNoun())

    def test_IsAdjective(self):
        self.assertTrue(self.parse2.isAdjective())
        self.assertTrue(self.parse3.isAdjective())
        self.assertTrue(self.parse6.isAdjective())

    def test_IsVerb(self):
        self.assertTrue(self.parse4.isVerb())
        self.assertTrue(self.parse8.isVerb())

    def test_IsRootVerb(self):
        self.assertTrue(self.parse2.isRootVerb())
        self.assertTrue(self.parse4.isRootVerb())
        self.assertTrue(self.parse5.isRootVerb())
        self.assertTrue(self.parse6.isRootVerb())

    def test_GetTreePos(self):
        self.assertEqual("NP", self.parse1.getTreePos())
        self.assertEqual("ADJP", self.parse2.getTreePos())
        self.assertEqual("ADJP", self.parse3.getTreePos())
        self.assertEqual("VP", self.parse4.getTreePos())
        self.assertEqual("NP", self.parse5.getTreePos())
        self.assertEqual("ADJP", self.parse6.getTreePos())
        self.assertEqual("NP", self.parse7.getTreePos())
        self.assertEqual("NEG", self.parse8.getTreePos())
        self.assertEqual("NOMP", self.parse9.getTreePos())


if __name__ == '__main__':
    unittest.main()
