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
        for state_node in root:
            state_name = state_node.attrib["name"]
            start_state = state_node.attrib["start"] == "yes"
            end_state = state_node.attrib["end"] == "yes"
            if start_state:
                original_pos = state_node.attrib["originalpos"]
                self.__states.append(State(state_name, True, end_state, original_pos))
            else:
                self.__states.append(State(state_name, False, end_state))
        for state_node in root:
            if "name" in state_node.attrib:
                state_name = state_node.attrib["name"]
                state = self.getState(state_name)
                for transition_node in state_node:
                    state_name = transition_node.attrib["name"]
                    if "transitionname" in transition_node.attrib:
                        with_name = transition_node.attrib["transitionname"]
                    else:
                        with_name = None
                    if "topos" in transition_node.attrib:
                        root_to_pos = transition_node.attrib["topos"]
                    else:
                        root_to_pos = None
                    to_state = self.getState(state_name)
                    if to_state is not None:
                        for with_node in transition_node:
                            if "name" in with_node.attrib:
                                with_name = with_node.attrib["name"]
                                if "topos" in with_node.attrib:
                                    to_pos = with_node.attrib["topos"]
                                else:
                                    to_pos = None
                            else:
                                to_pos = None
                            if to_pos is None:
                                if root_to_pos is None:
                                    self.addTransition(fromState=state,
                                                       toState=to_state,
                                                       _with=with_node.text,
                                                       withName=with_name)
                                else:
                                    self.addTransition(fromState=state,
                                                       toState=to_state,
                                                       _with=with_node.text,
                                                       withName=with_name,
                                                       toPos=root_to_pos)
                            else:
                                self.addTransition(fromState=state,
                                                   toState=to_state,
                                                   _with=with_node.text,
                                                   withName=with_name,
                                                   toPos=to_pos)

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

    def addTransition(self,
                      fromState: State,
                      toState: State,
                      _with: str,
                      withName: str,
                      toPos=None):
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
        new_transition = Transition(_with=_with,
                                    toState=toState,
                                    withName=withName,
                                    toPos=toPos)
        if fromState in self.__transitions:
            transition_list = self.__transitions[fromState]
        else:
            transition_list = []
        transition_list.append(new_transition)
        self.__transitions[fromState] = transition_list

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
