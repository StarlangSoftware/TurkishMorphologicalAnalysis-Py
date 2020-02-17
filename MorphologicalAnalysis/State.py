class State:

    __startState: bool
    __endState: bool
    __name: str
    __pos: str

    def __init__(self, name: str, startState: bool, endState: bool, pos=None):
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
        self.__endState = endState
        self.__startState = startState
        self.__name = name
        self.__pos = pos

    def __str__(self) -> str:
        """
        Overridden __str__ method which returns the name.

        RETURNS
        -------
        str
            String name.
        """
        return self.__name

    def getName(self) -> str:
        """
        Getter for the name.

        RETURNS
        -------
        str
            String name.
        """
        return self.__name

    def getPos(self) -> str:
        """
        Getter for the pos.

        RETURNS
        -------
        str
            String pos.
        """
        return self.__pos

    def isEndState(self) -> bool:
        """
        The isEndState method returns endState's value.

        RETURNS
        -------
        bool
            boolean endState.
        """
        return self.__endState
