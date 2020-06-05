import unittest

from MorphologicalAnalysis.InflectionalGroup import InflectionalGroup
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag


class InflectionalGroupTest(unittest.TestCase):

    def test_size(self):
        inflectionalGroup1 = InflectionalGroup("ADJ")
        self.assertEqual(1, inflectionalGroup1.size())
        inflectionalGroup2 = InflectionalGroup("ADJ+JUSTLIKE")
        self.assertEqual(2, inflectionalGroup2.size())
        inflectionalGroup3 = InflectionalGroup("ADJ+FUTPART+P1PL")
        self.assertEqual(3, inflectionalGroup3.size())
        inflectionalGroup4 = InflectionalGroup("NOUN+A3PL+P1PL+ABL")
        self.assertEqual(4, inflectionalGroup4.size())
        inflectionalGroup5 = InflectionalGroup("ADJ+WITH+A3SG+P3SG+ABL")
        self.assertEqual(5, inflectionalGroup5.size())
        inflectionalGroup6 = InflectionalGroup("VERB+ABLE+NEG+FUT+A3PL+COP")
        self.assertEqual(6, inflectionalGroup6.size())
        inflectionalGroup7 = InflectionalGroup("VERB+ABLE+NEG+AOR+A3SG+COND+A1SG")
        self.assertEqual(7, inflectionalGroup7.size())

    def test_containsCase(self):
        inflectionalGroup1 = InflectionalGroup("NOUN+ACTOF+A3PL+P1PL+NOM")
        self.assertIsNotNone(inflectionalGroup1.containsCase())
        inflectionalGroup2 = InflectionalGroup("NOUN+A3PL+P1PL+ACC")
        self.assertIsNotNone(inflectionalGroup2.containsCase())
        inflectionalGroup3 = InflectionalGroup("NOUN+ZERO+A3SG+P3PL+DAT")
        self.assertIsNotNone(inflectionalGroup3.containsCase())
        inflectionalGroup4 = InflectionalGroup("PRON+QUANTP+A1PL+P1PL+LOC")
        self.assertIsNotNone(inflectionalGroup4.containsCase())
        inflectionalGroup5 = InflectionalGroup("NOUN+AGT+A3SG+P2SG+ABL")
        self.assertIsNotNone(inflectionalGroup5.containsCase())

    def test_containsPlural(self):
        inflectionalGroup1 = InflectionalGroup("VERB+NEG+NECES+A1PL")
        self.assertTrue(inflectionalGroup1.containsPlural())
        inflectionalGroup2 = InflectionalGroup("PRON+PERS+A2PL+PNON+NOM")
        self.assertTrue(inflectionalGroup2.containsPlural())
        inflectionalGroup3 = InflectionalGroup("NOUN+DIM+A3PL+P2SG+GEN")
        self.assertTrue(inflectionalGroup3.containsPlural())
        inflectionalGroup4 = InflectionalGroup("NOUN+A3PL+P1PL+GEN")
        self.assertTrue(inflectionalGroup4.containsPlural())
        inflectionalGroup5 = InflectionalGroup("NOUN+ZERO+A3SG+P2PL+INS")
        self.assertTrue(inflectionalGroup5.containsPlural())
        inflectionalGroup6 = InflectionalGroup("PRON+QUANTP+A3PL+P3PL+LOC")
        self.assertTrue(inflectionalGroup6.containsPlural())

    def test_containsTag(self):
        inflectionalGroup1 = InflectionalGroup("NOUN+ZERO+A3SG+P1SG+NOM")
        self.assertTrue(inflectionalGroup1.containsTag(MorphologicalTag.NOUN))
        inflectionalGroup2 = InflectionalGroup("NOUN+AGT+A3PL+P2SG+ABL")
        self.assertTrue(inflectionalGroup2.containsTag(MorphologicalTag.AGENT))
        inflectionalGroup3 = InflectionalGroup("NOUN+INF2+A3PL+P3SG+NOM")
        self.assertTrue(inflectionalGroup3.containsTag(MorphologicalTag.NOMINATIVE))
        inflectionalGroup4 = InflectionalGroup("NOUN+ZERO+A3SG+P1PL+ACC")
        self.assertTrue(inflectionalGroup4.containsTag(MorphologicalTag.ZERO))
        inflectionalGroup5 = InflectionalGroup("NOUN+ZERO+A3SG+P2PL+INS")
        self.assertTrue(inflectionalGroup5.containsTag(MorphologicalTag.P2PL))
        inflectionalGroup6 = InflectionalGroup("PRON+QUANTP+A3PL+P3PL+LOC")
        self.assertTrue(inflectionalGroup6.containsTag(MorphologicalTag.QUANTITATIVEPRONOUN))

    def test_containsPossessive(self):
        inflectionalGroup1 = InflectionalGroup("NOUN+ZERO+A3SG+P1SG+NOM")
        self.assertTrue(inflectionalGroup1.containsPossessive())
        inflectionalGroup2 = InflectionalGroup("NOUN+AGT+A3PL+P2SG+ABL")
        self.assertTrue(inflectionalGroup2.containsPossessive())
        inflectionalGroup3 = InflectionalGroup("NOUN+INF2+A3PL+P3SG+NOM")
        self.assertTrue(inflectionalGroup3.containsPossessive())
        inflectionalGroup4 = InflectionalGroup("NOUN+ZERO+A3SG+P1PL+ACC")
        self.assertTrue(inflectionalGroup4.containsPossessive())
        inflectionalGroup5 = InflectionalGroup("NOUN+ZERO+A3SG+P2PL+INS")
        self.assertTrue(inflectionalGroup5.containsPossessive())
        inflectionalGroup6 = InflectionalGroup("PRON+QUANTP+A3PL+P3PL+LOC")
        self.assertTrue(inflectionalGroup6.containsPossessive())


if __name__ == '__main__':
    unittest.main()
