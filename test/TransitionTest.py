import unittest

from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer


class TransitionTest(unittest.TestCase):

    fsm : FsmMorphologicalAnalyzer

    def setUp(self) -> None:
        self.fsm = FsmMorphologicalAnalyzer()

    def test_NumberWithAccusative(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("2'yi").size() != 0)
        self.assertEqual(0, self.fsm.morphologicalAnalysis("2'i").size())
        self.assertTrue(self.fsm.morphologicalAnalysis("5'i").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("9'u").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("10'u").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("30'u").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("3'ü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("4'ü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("100'ü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("6'yı").size() != 0)
        self.assertEqual(0, self.fsm.morphologicalAnalysis("6'ı").size())
        self.assertTrue(self.fsm.morphologicalAnalysis("40'ı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("60'ı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("90'ı").size() != 0)

    def test_NumberWithDative(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("6'ya").size() != 0)
        self.assertEqual(0, self.fsm.morphologicalAnalysis("6'a").size())
        self.assertTrue(self.fsm.morphologicalAnalysis("9'a").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("10'a").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("30'a").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("40'a").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("60'a").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("90'a").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("2'ye").size() != 0)
        self.assertEqual(0, self.fsm.morphologicalAnalysis("2'e").size())
        self.assertTrue(self.fsm.morphologicalAnalysis("8'e").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("5'e").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("4'e").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("1'e").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("3'e").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("7'ye").size() != 0)
        self.assertEqual(0, self.fsm.morphologicalAnalysis("7'e").size())

    def test_PresentTense(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("büyülüyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("bölümlüyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("buğuluyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("bulguluyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("açıklıyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("çalkalıyor").size() != 0)

    def test_A(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("saatinizi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("alkole").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("anormale").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("sakala").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("kabala").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("faika").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("halika").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("kediye").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("eve").size() != 0)

    def test_C(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("gripçi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("güllaççı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("gülütçü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("gülükçü").size() != 0)

    def test_SH(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("altışar").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("yedişer").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("üçer").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("beşer").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("dörder").size() != 0)

    def test_NumberWithD(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("1'di").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("2'ydi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("3'tü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("4'tü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("5'ti").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("6'ydı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("7'ydi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("8'di").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("9'du").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("30'du").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("40'tı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("60'tı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("70'ti").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("50'ydi").size() != 0)

    def test_D(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("koştu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("kitaptı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("kaçtı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("evdi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("fraktı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("sattı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("aftı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("kesti").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ahtı").size() != 0)

    def test_Exceptions(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("yiyip").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("sana").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("bununla").size() != 0)
        self.assertEqual(0, self.fsm.morphologicalAnalysis("buyla").size())
        self.assertTrue(self.fsm.morphologicalAnalysis("onunla").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("şununla").size() != 0)
        self.assertEqual(0, self.fsm.morphologicalAnalysis("şuyla").size())
        self.assertTrue(self.fsm.morphologicalAnalysis("bana").size() != 0)

    def test_VowelEChangesToIDuringYSuffixation(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("diyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("yiyor").size() != 0)

    def test_LastIdropsDuringPassiveSuffixation(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("yoğruldu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("buyruldu").size() != 0)

    def test_ShowsSuRegularities(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("karasuyu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("suyu").size() != 0)

    def test_DuplicatesDuringSuffixation(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("tıbbı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ceddi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("zıddı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("serhaddi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("fenni").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("haddi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("hazzı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("şakkı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("şakı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("halli").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("hali").size() != 0)

    def test_LastIdropsDuringSuffixation(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("hizbi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("kaybı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ahdi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("nesci").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("zehri").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("zikri").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("metni").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("metini").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("katli").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("katili").size() != 0)

    def test_NounSoftenDuringSuffixation(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("adabı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("amibi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("armudu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ağacı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("akacı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("arkeoloğu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("filoloğu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ahengi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("küngü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("kitaplığı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("küllüğü").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("adedi").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("adeti").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ağıdı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ağıtı").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("anotu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("anodu").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("Kuzguncuk'u").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("Leylak'ı").size() != 0)

    def test_VerbSoftenDuringSuffixation(self):
        self.assertTrue(self.fsm.morphologicalAnalysis("cezbediyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("ediyor").size() != 0)
        self.assertTrue(self.fsm.morphologicalAnalysis("bahsediyor").size() != 0)


if __name__ == '__main__':
    unittest.main()
