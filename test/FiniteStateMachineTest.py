import unittest

from DataStructure.CounterHashMap import CounterHashMap

from MorphologicalAnalysis.FiniteStateMachine import FiniteStateMachine


class FiniteStateMachineTest(unittest.TestCase):

    fsm : FiniteStateMachine
    stateList : list

    def setUp(self) -> None:
        self.fsm = FiniteStateMachine("../MorphologicalAnalysis/data/turkish_finite_state_machine.xml")
        self.stateList = self.fsm.getStates()

    def test_StateCount(self):
        self.assertEqual(141, len(self.stateList))

    def test_StartEndStates(self):
        endStateCount = 0
        for state in self.stateList:
            if state.isEndState():
                endStateCount = endStateCount + 1
        self.assertEqual(37, endStateCount)
        posCounts = CounterHashMap()
        for state in self.stateList:
            posCounts.put(state.getPos())
        self.assertEqual(1, posCounts.get("HEAD"))
        self.assertEqual(6, posCounts.get("PRON"))
        self.assertEqual(1, posCounts.get("PROP"))
        self.assertEqual(8, posCounts.get("NUM"))
        self.assertEqual(7, posCounts.get("ADJ"))
        self.assertEqual(1, posCounts.get("INTERJ"))
        self.assertEqual(1, posCounts.get("DET"))
        self.assertEqual(1, posCounts.get("ADVERB"))
        self.assertEqual(1, posCounts.get("QUES"))
        self.assertEqual(1, posCounts.get("CONJ"))
        self.assertEqual(26, posCounts.get("VERB"))
        self.assertEqual(1, posCounts.get("POSTP"))
        self.assertEqual(1, posCounts.get("DUP"))
        self.assertEqual(11, posCounts.get("NOUN"))

    def test_TransitionCount(self):
        transitionCount = 0
        for state in self.stateList:
            transitionCount += len(self.fsm.getTransitions(state))
        self.assertEqual(779, transitionCount)

    def test_TransitionWith(self):
        transitionCounts = CounterHashMap()
        for state in self.stateList:
            transitions = self.fsm.getTransitions(state)
            for transition in transitions:
                transitionCounts.put(transition.__str__())
        topList = transitionCounts.topN(5)
        self.assertEqual("0", topList[0][1])
        self.assertEqual(111, topList[0][0])
        self.assertEqual("lAr", topList[1][1])
        self.assertEqual(37, topList[1][0])
        self.assertEqual("DHr", topList[2][1])
        self.assertEqual(28, topList[2][0])
        self.assertEqual("Hn", topList[3][1])
        self.assertEqual(24, topList[3][0])
        self.assertEqual("lArH", topList[4][1])
        self.assertEqual(23, topList[4][0])

    def test_TransitionWithName(self):
        transitionCounts = CounterHashMap()
        for state in self.stateList:
            transitions = self.fsm.getTransitions(state)
            for transition in transitions:
                transitionCounts.put(transition.withName())
        topList = transitionCounts.topN(5)
        self.assertEqual(None, topList[0][1])
        self.assertEqual(52, topList[0][0])
        self.assertEqual("^DB+VERB+CAUS", topList[1][1])
        self.assertEqual(33, topList[1][0])
        self.assertEqual("^DB+VERB+PASS", topList[2][1])
        self.assertEqual(31, topList[2][0])
        self.assertEqual("A3PL", topList[3][1])
        self.assertEqual(28, topList[3][0])
        self.assertEqual("LOC", topList[4][1])
        self.assertEqual(24, topList[4][0])

if __name__ == '__main__':
    unittest.main()
