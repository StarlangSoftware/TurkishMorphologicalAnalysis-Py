class State:

    __startState: bool
    __endState: bool
    __name: str
    __pos: str

    """
    Second constructor of the State class which takes 4 parameters as input; String name, boolean startState,
    boolean endState, and String pos and initializes the private variables of the class.

    PARAMETERS
    ----------
    name : str
        String input.
    startState : bool
        boolean input.
    endState : bool  
        boolean input.
    pos : str
        String input.
    """
    def __init__(self, name: str, startState: bool, endState: bool, pos=None):
        self.__endState = endState
        self.__startState = startState
        self.__name = name
        self.__pos = pos

    """
    Overridden __str__ method which returns the name.

    RETURNS
    -------
    str
        String name.
    """
    def __str__(self) -> str:
        return self.__name

    """
    Getter for the name.

    RETURNS
    -------
    str
        String name.
    """
    def getName(self) -> str:
        return self.__name

    """
    Getter for the pos.

    RETURNS
    -------
    str
        String pos.
    """
    def getPos(self) -> str:
        return self.__pos

    """
    The isEndState method returns endState's value.

    RETURNS
    -------
    bool
        boolean endState.
    """
    def isEndState(self) -> bool:
        return self.__endState
