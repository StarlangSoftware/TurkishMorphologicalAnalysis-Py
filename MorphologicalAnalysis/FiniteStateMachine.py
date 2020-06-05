import xml.etree.ElementTree

from MorphologicalAnalysis.State import State
from MorphologicalAnalysis.Transition import Transition


class FiniteStateMachine:

    __states: list
    __transitions: dict

    def __init__(self, fileName: str):
        """
        Constructor reads the finite state machine in the given input file. It has a NodeList which holds the states
        of the nodes and there are 4 different type of nodes; stateNode, root Node, transitionNode and withNode.
        Also there are two states; state that a node currently in and state that a node will be in.

        XMLParser is used to parse the given file. Firstly it gets the document to parse, then gets its elements by the
        tag names. For instance, it gets states by the tag name 'state' and puts them into an ArrayList called
        stateList.
        Secondly, it traverses this stateList and gets each Node's attributes. There are three attributes; name, start,
        and end which will be named as states. If a node is in a startState it is tagged as 'yes', otherwise 'no'.
        Also, if a node is in a startState, additional attribute will be fetched; originalPos that represents its
        original part of speech.

        At the last step, by starting rootNode's first child, it gets all the transitionNodes and next states called
        toState then continue with the nextSiblings. Also, if there is no possible toState, it prints this case and the
        causative states.

        PARAMETERS
        ----------
        fileName : str
            the resource file to read the finite state machine. Only files in resources folder are supported.
        """
        self.__transitions = {}
        self.__states = []
        root = xml.etree.ElementTree.parse(fileName).getroot()
        for stateNode in root:
            stateName = stateNode.attrib["name"]
            startState = stateNode.attrib["start"] == "yes"
            endState = stateNode.attrib["end"] == "yes"
            if startState:
                originalPos = stateNode.attrib["originalpos"]
                self.__states.append(State(stateName, True, endState, originalPos))
            else:
                self.__states.append(State(stateName, False, endState))
        for stateNode in root:
            if "name" in stateNode.attrib:
                stateName = stateNode.attrib["name"]
                state = self.getState(stateName)
                for transitionNode in stateNode:
                    stateName = transitionNode.attrib["name"]
                    if "transitionname" in transitionNode.attrib:
                        withName = transitionNode.attrib["transitionname"]
                    else:
                        withName = None
                    if "topos" in transitionNode.attrib:
                        rootToPos = transitionNode.attrib["topos"]
                    else:
                        rootToPos = None
                    toState = self.getState(stateName)
                    if toState is not None:
                        for withNode in transitionNode:
                            if "name" in withNode.attrib:
                                withName = withNode.attrib["name"]
                                if "topos" in withNode.attrib:
                                    toPos = withNode.attrib["topos"]
                                else:
                                    toPos = None
                            else:
                                toPos = None
                            if toPos is None:
                                if rootToPos is None:
                                    self.addTransition(state, toState, withNode.text, withName)
                                else:
                                    self.addTransition(state, toState, withNode.text, withName, rootToPos)
                            else:
                                self.addTransition(state, toState, withNode.text, withName, toPos)

    def isValidTransition(self, transition: str) -> bool:
        """
        The isValidTransition loops through states ArrayList and checks transitions between states. If the actual
        transition equals to the given transition input, method returns true otherwise returns false.

        PARAMETERS
        ----------
        transition : str
            is used to compare with the actual transition of a state.

        RETURNS
        -------
        bool
            True when the actual transition equals to the transition input, false otherwise.
        """
        for state in self.__transitions.keys():
            for transition1 in self.__transitions[state]:
                if transition1.__str__() is not None and transition1.__str__() == transition:
                    return True
        return False

    def getStates(self) -> list:
        """
        The getStates method returns the states in the FiniteStateMachine.
        RETURNS
        -------
        list
             StateList.
        """
        return self.__states

    def getState(self, name: str) -> State:
        """
        The getState method is used to loop through the states list and return the state whose name equal
        to the given input name.

        PARAMETERS
        ----------
        name : str
            is used to compare with the state's actual name.

        RETURNS
        -------
        State
            State if found any, None otherwise.
        """
        for state in self.__states:
            if state.getName() == name:
                return state
        return None

    def addTransition(self, fromState: State, toState: State, _with: str, withName: str, toPos=None):
        """
        Another addTransition method which takes additional argument; toPos and. It creates a new Transition
        with given input parameters and adds the transition to transitions list.

        PARAMETERS
        ----------
        fromState : State
            State type input indicating the previous state.
        toState : State
            State type input indicating the next state.
        _with : str
            String input indicating with what the transition will be made.
        withName : str
            String input.
        toPos : str
            String input.
        """
        newTransition = Transition(_with, toState, withName, toPos)
        if fromState in self.__transitions:
            transitionList = self.__transitions[fromState]
        else:
            transitionList = []
        transitionList.append(newTransition)
        self.__transitions[fromState] = transitionList

    def getTransitions(self, state: State) -> list:
        """
        The getTransitions method returns the transitions at the given state.

        PARAMETERS
        ----------
        state : State
            State input.

        RETURNS
        -------
        list
            Transitions at given state.
        """
        if state in self.__transitions:
            return self.__transitions[state]
        else:
            return []
