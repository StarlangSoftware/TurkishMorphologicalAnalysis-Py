import unittest

from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalAnalysis.FsmParse import FsmParse


class FsmParseTest(unittest.TestCase):

    parse1 : FsmParse 
    parse2 : FsmParse 
    parse3 : FsmParse 
    parse4 : FsmParse 
    parse5 : FsmParse 
    parse6 : FsmParse 
    parse7 : FsmParse 
    parse8 : FsmParse 
    parse9 : FsmParse

    def setUp(self) -> None:
        self.fsm = FsmMorphologicalAnalyzer("../turkish_dictionary.txt", "../turkish_misspellings.txt", "../turkish_finite_state_machine.xml")
        self.parse1 = self.fsm.morphologicalAnalysis("açılır").getFsmParse(0)
        self.parse2 = self.fsm.morphologicalAnalysis("koparılarak").getFsmParse(0)
        self.parse3 = self.fsm.morphologicalAnalysis("toplama").getFsmParse(0)
        self.parse4 = self.fsm.morphologicalAnalysis("değerlendirmede").getFsmParse(0)
        self.parse5 = self.fsm.morphologicalAnalysis("soruşturmasının").getFsmParse(0)
        self.parse6 = self.fsm.morphologicalAnalysis("karşılaştırmalı").getFsmParse(0)
        self.parse7 = self.fsm.morphologicalAnalysis("esaslarını").getFsmParse(0)
        self.parse8 = self.fsm.morphologicalAnalysis("güçleriyle").getFsmParse(0)
        self.parse9 = self.fsm.morphologicalAnalysis("bulmayacakları").getFsmParse(0)

    def  test_GetLastLemmaWithTag(self):
        self.assertEqual("açıl", self.parse1.getLastLemmaWithTag("VERB"))
        self.assertEqual("koparıl", self.parse2.getLastLemmaWithTag("VERB"))
        self.assertEqual("değerlendir", self.parse4.getLastLemmaWithTag("VERB"))
        self.assertEqual("soruştur", self.parse5.getLastLemmaWithTag("VERB"))
        self.assertEqual("karşı", self.parse6.getLastLemmaWithTag("ADJ"))

    def test_GetLastLemma(self):
        self.assertEqual("açıl", self.parse1.getLastLemma())
        self.assertEqual("koparılarak", self.parse2.getLastLemma())
        self.assertEqual("değerlendirme", self.parse4.getLastLemma())
        self.assertEqual("soruşturma", self.parse5.getLastLemma())
        self.assertEqual("karşılaştır", self.parse6.getLastLemma())

    def test_GetTransitionList(self):
        self.assertEqual("aç+VERB^DB+VERB+PASS+POS+AOR+A3SG", self.parse1.__str__())
        self.assertEqual("kop+VERB^DB+VERB+CAUS^DB+VERB+PASS+POS^DB+ADV+BYDOINGSO", self.parse2.__str__())
        self.assertEqual("topla+NOUN+A3SG+P1SG+DAT", self.parse3.__str__())
        self.assertEqual("değer+NOUN+A3SG+PNON+NOM^DB+VERB+ACQUIRE^DB+VERB+CAUS+POS^DB+NOUN+INF2+A3SG+PNON+LOC", self.parse4.__str__())
        self.assertEqual("sor+VERB+RECIP^DB+VERB+CAUS+POS^DB+NOUN+INF2+A3SG+P3SG+GEN", self.parse5.__str__())
        self.assertEqual("karşı+ADJ^DB+VERB+BECOME^DB+VERB+CAUS+POS+NECES+A3SG", self.parse6.__str__())
        self.assertEqual("esas+ADJ^DB+NOUN+ZERO+A3PL+P2SG+ACC", self.parse7.__str__())
        self.assertEqual("güç+ADJ^DB+NOUN+ZERO+A3PL+P3PL+INS", self.parse8.__str__())
        self.assertEqual("bul+VERB+NEG^DB+ADJ+FUTPART+P3PL", self.parse9.__str__())

    def test_WithList(self):
        self.assertEqual("aç+Hl+Hr", self.parse1.withList())
        self.assertEqual("kop+Ar+Hl+yArAk", self.parse2.withList())
        self.assertEqual("topla+Hm+yA", self.parse3.withList())
        self.assertEqual("değer+lAn+DHr+mA+DA", self.parse4.withList())
        self.assertEqual("sor+Hs+DHr+mA+sH+nHn", self.parse5.withList())
        self.assertEqual("karşı+lAs+DHr+mAlH", self.parse6.withList())
        self.assertEqual("esas+lAr+Hn+yH", self.parse7.withList())
        self.assertEqual("güç+lArH+ylA", self.parse8.withList())
        self.assertEqual("bul+mA+yAcAk+lArH", self.parse9.withList())

    def test_SuffixList(self):
        self.assertEqual("VerbalRoot(F5PR)(aç)+PassiveHl(açıl)+OtherTense2(açılır)", self.parse1.suffixList())
        self.assertEqual("VerbalRoot(F1P1)(kop)+CausativeAr(kopar)+PassiveHl(koparıl)+Adverb1(koparılarak)", self.parse2.suffixList())
        self.assertEqual("NominalRoot(topla)+Possessive(toplam)+Case1(toplama)", self.parse3.suffixList())
        self.assertEqual("NominalRoot(değer)+VerbalRoot(F5PR)(değerlen)+CausativeDHr(değerlendir)+NominalRoot(değerlendirme)+Case1(değerlendirmede)", self.parse4.suffixList())
        self.assertEqual("VerbalRoot(F5PR)(sor)+Reciprocal(soruş)+CausativeDHr(soruştur)+NominalRoot(soruşturma)+Possessive3(soruşturması)+Case1(soruşturmasının)", self.parse5.suffixList())
        self.assertEqual("AdjectiveRoot(karşı)+VerbalRoot(F5PR)(karşılaş)+CausativeDHr(karşılaştır)+OtherTense(karşılaştırmalı)", self.parse6.suffixList())
        self.assertEqual("AdjectiveRoot(esas)+Plural(esaslar)+Possessive(esasların)+AccusativeNoun(esaslarını)", self.parse7.suffixList())
        self.assertEqual("AdjectiveRoot(güç)+Possesive3(güçleri)+Case1(güçleriyle)", self.parse8.suffixList())
        self.assertEqual("VerbalRoot(F5PW)(bul)+Negativema(bulma)+AdjectiveParticiple(bulmayacak)+Adjective(bulmayacakları)", self.parse9.suffixList())

if __name__ == '__main__':
    unittest.main()
