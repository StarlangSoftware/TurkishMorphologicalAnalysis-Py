from Dictionary.Word import Word

from MorphologicalAnalysis.FsmParse import FsmParse


class FsmParseList:
    __fsmParses: list

    def __init__(self, fsmParses: list):
        """
        A constructor of FsmParseList class which takes a list fsmParses as an input. First it sorts
        the items of the list then loops through it, if the current item's transitions equal to the next item's
        transitions, it removes the latter item. At the end, it assigns this list to the fsmParses variable.

        PARAMETERS
        ----------
        fsmParses : list
            FsmParse list input.
        """
        fsmParses.sort()
        i = 0
        while i < len(fsmParses) - 1:
            if fsmParses[i].transitionList() == fsmParses[i + 1].transitionList():
                fsmParses.pop(i + 1)
                i = i - 1
            i = i + 1
        self.__fsmParses = fsmParses

    def size(self) -> int:
        """
        The size method returns the size of fsmParses list.

        RETURNS
        -------
        int
            The size of fsmParses list.
        """
        return len(self.__fsmParses)

    def getFsmParse(self, index: int) -> FsmParse:
        """
        The getFsmParse method takes an integer index as an input and returns the item of fsmParses list at given index.

        PARAMETERS
        ----------
        index : int
            Integer input.

        RETURNS
        -------
        FsmParse
            The item of fsmParses list at given index.
        """
        return self.__fsmParses[index]

    def rootWords(self) -> str:
        """
        The rootWords method gets the first item's root of fsmParses list and uses it as currentRoot. Then loops through
        the fsmParses, if the current item's root does not equal to the currentRoot, it then assigns it as the
        currentRoot and accumulates root words in a string result.

        RETURNS
        -------
        str
            String result that has root words.
        """
        result = self.__fsmParses[0].getWord().getName()
        currentRoot = result
        for i in range(1, len(self.__fsmParses)):
            if self.__fsmParses[i].getWord().getName() != currentRoot:
                currentRoot = self.__fsmParses[i].getWord().getName()
                result = result + "$" + currentRoot
        return result

    def reduceToParsesWithSameRootAndPos(self, currentWithPos: Word):
        """
        The reduceToParsesWithSameRootAndPos method takes a Word} currentWithPos as an input and loops i times till
        i equals to the size of the fsmParses list. If the given currentWithPos does not equal to the ith item's
        root and the MorphologicalTag of the first inflectional of fsmParses, it removes the ith item from the list.

        PARAMETERS
        ----------
        currentWithPos : Word
            Word input.
        """
        i = 0
        while i < len(self.__fsmParses):
            if self.__fsmParses[i].getWordWithPos() != currentWithPos:
                self.__fsmParses.pop(i)
            else:
                i = i + 1

    def getParseWithLongestRootWord(self) -> FsmParse:
        """
        The getParseWithLongestRootWord method returns the parse with the longest root word. If more than one parse has
        the longest root word, the first parse with that root is returned.
        RETURNS
        -------
        FsmParse
            Parse with the longest root word.
        """
        maxLength = -1
        bestParse = None
        for currentParse in self.__fsmParses:
            if len(currentParse.getWord().getName()) > maxLength:
                maxLength = len(currentParse.getWord().getName())
                bestParse = currentParse
        return bestParse

    def reduceToParsesWithSameRoot(self, currentRoot: str):
        """
        The reduceToParsesWithSameRoot method takes a str currentWithPos as an input and loops i times till
        i equals to the size of the fsmParses list. If the given currentRoot does not equal to the root of ith item of
        fsmParses, it removes the ith item from the list.

        PARAMETERS
        ----------
        currentRoot : str
            String input.
        """
        i = 0
        while i < len(self.__fsmParses):
            if self.__fsmParses[i].getWord().getName() != currentRoot:
                self.__fsmParses.pop(i)
            else:
                i = i + 1

    def constructParseListForDifferentRootWithPos(self) -> list:
        """
        The constructParseListForDifferentRootWithPos method initially creates a result list then loops through the
        fsmParses list. For the first iteration, it creates new list as initial, then adds the
        first item od fsmParses to initial and also add this initial list to the result list. For the following
        iterations,
        it checks whether the current item's root with the MorphologicalTag of the first inflectional
        equal to the previous item's  root with the MorphologicalTag of the first inflectional. If so, it adds that item
        to the result list, if not it creates new list as initial and adds the first item od fsmParses
        to initial and also add this initial list to the result list.

        RETURNS
        -------
        result : list
            list type of FsmParseList.
        """
        result = []
        i = 0
        while i < len(self.__fsmParses):
            if i == 0:
                initial = [self.__fsmParses[i]]
                result.append(FsmParseList(initial))
            else:
                if self.__fsmParses[i].getWordWithPos() == self.__fsmParses[i - 1].getWordWithPos():
                    result[len(result) - 1].__fsmParses.append(self.__fsmParses[i])
                else:
                    initial = [self.__fsmParses[i]]
                    result.append(FsmParseList(initial))
            i = i + 1
        return result

    def parsesWithoutPrefixAndSuffix(self) -> str:
        """
        The parsesWithoutPrefixAndSuffix method first creates a str array named analyses with the size of fsmParses
        list's size.

        If the size is just 1, it then returns the first item's transitionList, if it is greater than 1, loops through
        the fsmParses and puts the transitionList of each item to the analyses array.

        If the removePrefix condition holds, it loops through the analyses array and takes each item's substring after
        the first + sign and updates that item of analyses array with that substring.

        If the removeSuffix condition holds, it loops through the analyses array and takes each item's substring till
        the last + sign and updates that item of analyses array with that substring.

        It then removes the duplicate items of analyses array and returns a result str that has the accumulated items of
        analyses array.

        RETURNS
        -------
        str
            result str that has the accumulated items of analyses array.
        """
        analyses = [""] * len(self.__fsmParses)
        removePrefix = True
        removeSuffix = True
        if len(self.__fsmParses) == 1:
            return self.__fsmParses[0].transitionList()[self.__fsmParses[0].transitionList().index("+") + 1]
        for i in range(len(self.__fsmParses)):
            analyses[i] = self.__fsmParses[i].transitionList()
        while removePrefix:
            removePrefix = True
            for i in range(len(self.__fsmParses) - 1):
                if "+" not in analyses[i] or "+" not in analyses[i + 1] or \
                        analyses[i][:analyses[i].index("+") + 1] != analyses[i + 1][:analyses[i + 1].index("+") + 1]:
                    removePrefix = False
                    break
            if removePrefix:
                for i in range(len(self.__fsmParses)):
                    analyses[i] = analyses[i][analyses[i].index("+") + 1:]
        while removeSuffix:
            removeSuffix = True
            for i in range(len(self.__fsmParses) - 1):
                if "+" not in analyses[i] or "+" not in analyses[i + 1] or \
                        analyses[i][analyses[i].rindex("+") + 1] != analyses[i + 1][analyses[i + 1].rindex("+") + 1]:
                    removeSuffix = False
                    break
            if removeSuffix:
                for i in range(len(self.__fsmParses)):
                    analyses[i] = analyses[i][:analyses[i].rindex("+")]
        for i in range(len(analyses)):
            for j in range(i + 1, len(analyses)):
                if analyses[i] > analyses[j]:
                    analyses[i], analyses[j] = analyses[j], analyses[i]
        result = analyses[0]
        for i in range(1, len(analyses)):
            result = result + "$" + analyses[i]
        return result

    def __str__(self) -> str:
        """
        The overridden toString method loops through the fsmParses list and accumulates the items to a result str.

        RETURNS
        -------
        str
            Result str that has the items of fsmParses list.
        """
        result = ""
        for i in range(len(self.__fsmParses)):
            result += self.__fsmParses[i] + "\n"
        return result
