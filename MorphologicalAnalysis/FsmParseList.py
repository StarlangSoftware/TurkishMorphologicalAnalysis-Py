from Dictionary.Word import Word

from MorphologicalAnalysis.FsmParse import FsmParse


class FsmParseList:
    __fsmParses: list
    longestRootExceptions = [
        "acağı acak NOUN VERB", "acağım acak NOUN VERB", "acağımı acak NOUN VERB", "acağımız acak NOUN VERB",
        "acağın acak NOUN VERB",
        "acağına acak NOUN VERB", "acağını acak NOUN VERB", "acağının acak NOUN VERB", "acağınız acak NOUN VERB",
        "acağınıza acak NOUN VERB",
        "acağınızdır acak NOUN VERB", "acağınızı acak NOUN VERB", "acağınızın acak NOUN VERB", "acağız acak NOUN VERB",
        "acakları acak NOUN VERB",
        "acaklarını acak NOUN VERB", "acaksa acak NOUN VERB", "acaktır acak NOUN VERB", "ardım ar NOUN VERB",
        "arız ar NOUN VERB",
        "arken ar NOUN VERB", "arsa ar NOUN VERB", "arsak ar NOUN VERB", "arsanız ar NOUN VERB", "arsınız ar NOUN VERB",
        "eceği ecek NOUN VERB", "eceğim ecek NOUN VERB", "eceğimi ecek NOUN VERB", "eceğimiz ecek NOUN VERB",
        "eceğin ecek NOUN VERB",
        "eceğine ecek NOUN VERB", "eceğini ecek NOUN VERB", "eceğinin ecek NOUN VERB", "eceğiniz ecek NOUN VERB",
        "eceğinizdir ecek NOUN VERB",
        "eceğinize ecek NOUN VERB", "eceğinizi ecek NOUN VERB", "eceğinizin ecek NOUN VERB", "eceğiz ecek NOUN VERB",
        "ecekleri ecek NOUN VERB",
        "eceklerini ecek NOUN VERB", "ecekse ecek NOUN VERB", "ecektir ecek NOUN VERB", "erdim er NOUN VERB",
        "eriz er NOUN VERB",
        "erken er NOUN VERB", "erse er NOUN VERB", "ersek er NOUN VERB", "erseniz er NOUN VERB", "ersiniz er NOUN VERB",
        "ilen i VERB VERB", "ilene i VERB VERB", "ilin i VERB VERB", "ilince i VERB VERB", "imiz i ADJ NOUN",
        "in i ADJ NOUN", "inde i ADJ NOUN", "ine i ADJ NOUN", "ini i ADJ NOUN", "inin i ADJ NOUN",
        "ılan ı NOUN VERB", "ılana ı NOUN VERB", "ılın ı NOUN VERB", "ılınca ı NOUN VERB", "la la VERB NOUN",
        "lar la VERB NOUN", "lardan la VERB NOUN", "lardandır la VERB NOUN", "lardır la VERB NOUN", "ları la VERB NOUN",
        "larıdır la VERB NOUN", "larım la VERB NOUN", "larımdan la VERB NOUN", "larımız la VERB NOUN",
        "larımıza la VERB NOUN",
        "larımızda la VERB NOUN", "larımızdan la VERB NOUN", "larımızdaydı la VERB NOUN", "larımızı la VERB NOUN",
        "larımızın la VERB NOUN",
        "larımızla la VERB NOUN", "ların la VERB NOUN", "larına la VERB NOUN", "larında la VERB NOUN",
        "larındaki la VERB NOUN",
        "larındakiler la VERB NOUN", "larındakilere la VERB NOUN", "larındakileri la VERB NOUN",
        "larındakilerin la VERB NOUN", "larından la VERB NOUN",
        "larındandır la VERB NOUN", "larındaysa la VERB NOUN", "larını la VERB NOUN", "larının la VERB NOUN",
        "larınız la VERB NOUN",
        "larınıza la VERB NOUN", "larınızda la VERB NOUN", "larınızdaki la VERB NOUN", "larınızdan la VERB NOUN",
        "larınızı la VERB NOUN",
        "larınızın la VERB NOUN", "larınızla la VERB NOUN", "larıyla la VERB NOUN", "le le VERB NOUN",
        "ler le VERB NOUN",
        "lerden le VERB NOUN", "lerdendir le VERB NOUN", "lerdir le VERB NOUN", "leri le VERB NOUN",
        "leridir le VERB NOUN",
        "lerim le VERB NOUN", "lerimden le VERB NOUN", "lerimiz le VERB NOUN", "lerimizde le VERB NOUN",
        "lerimizden le VERB NOUN",
        "lerimizdeydi le VERB NOUN", "lerimize le VERB NOUN", "lerimizi le VERB NOUN", "lerimizin le VERB NOUN",
        "lerimizle le VERB NOUN",
        "lerin le VERB NOUN", "lerinde le VERB NOUN", "lerindeki le VERB NOUN", "lerindekiler le VERB NOUN",
        "lerindekilere le VERB NOUN",
        "lerindekileri le VERB NOUN", "lerindekilerin le VERB NOUN", "lerinden le VERB NOUN",
        "lerindendir le VERB NOUN", "lerindeyse le VERB NOUN",
        "lerine le VERB NOUN", "lerini le VERB NOUN", "lerinin le VERB NOUN", "leriniz le VERB NOUN",
        "lerinizde le VERB NOUN",
        "lerinizdeki le VERB NOUN", "lerinizden le VERB NOUN", "lerinize le VERB NOUN", "lerinizi le VERB NOUN",
        "lerinizin le VERB NOUN",
        "lerinizle le VERB NOUN", "leriyle le VERB NOUN", "madan ma NOUN VERB", "malı ma NOUN VERB",
        "malıdır ma NOUN VERB", "malıdırlar ma NOUN VERB", "malılar ma NOUN VERB", "malısınız ma NOUN VERB",
        "malıyım ma NOUN VERB",
        "malıyız ma NOUN VERB", "mam ma NOUN VERB", "mama ma NOUN VERB", "mamız ma NOUN VERB", "mamıza ma NOUN VERB",
        "mamızı ma NOUN VERB", "manız ma NOUN VERB", "manızda ma NOUN VERB", "manızdır ma NOUN VERB",
        "manızı ma NOUN VERB",
        "manızla ma NOUN VERB", "ması ma NOUN VERB", "masıdır ma NOUN VERB", "masın ma NOUN VERB",
        "masına ma NOUN VERB",
        "masında ma NOUN VERB", "masındaki ma NOUN VERB", "masını ma NOUN VERB", "masıyla ma NOUN VERB",
        "mdan m NOUN NOUN",
        "meden me NOUN VERB", "meli me NOUN VERB", "melidir me NOUN VERB", "melidirler me NOUN VERB",
        "meliler me NOUN VERB",
        "melisiniz me NOUN VERB", "meliyim me NOUN VERB", "meliyiz me NOUN VERB", "mem me NOUN VERB",
        "meme me NOUN VERB",
        "memiz me NOUN VERB", "memize me NOUN VERB", "memizi me NOUN VERB", "meniz me NOUN VERB",
        "menizde me NOUN VERB",
        "menizdir me NOUN VERB", "menizi me NOUN VERB", "menizle me NOUN VERB", "mesi me NOUN VERB",
        "mesidir me NOUN VERB",
        "mesin me NOUN VERB", "mesinde me NOUN VERB", "mesindeki me NOUN VERB", "mesine me NOUN VERB",
        "mesini me NOUN VERB",
        "mesiyle me NOUN VERB", "mişse miş NOUN VERB", "mını m NOUN NOUN", "mışsa mış NOUN VERB", "mız m NOUN NOUN",
        "na n NOUN NOUN", "ne n NOUN NOUN", "nin n NOUN NOUN", "niz n NOUN NOUN",
        "nın n NOUN NOUN", "nız n NOUN NOUN", "rdim r NOUN VERB", "rdım r NOUN VERB", "riz r NOUN VERB",
        "rız r NOUN VERB", "rken r NOUN VERB", "rken r NOUN VERB", "rsa r NOUN VERB", "rsak r NOUN VERB",
        "rsanız r NOUN VERB", "rse r NOUN VERB", "rsek r NOUN VERB", "rseniz r NOUN VERB", "rsiniz r NOUN VERB",
        "rsınız r NOUN VERB", "sa sa VERB ADJ", "se se VERB ADJ", "ulan u NOUN VERB", "un un VERB NOUN",
        "üne ün VERB NOUN", "unun un VERB NOUN", "ince i NOUN VERB", "unca u NOUN VERB", "ınca ı NOUN VERB",
        "unca un NOUN VERB", "ilen ile VERB VERB"]

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
        The reduceToParsesWithSameRootAndPos method takes a Word currentWithPos as an input and loops i times till
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
        the longest root word, the first parse with that root is returned. If the longest root word belongs to an
        exceptional case, the parse with the next longest root word that does not, is returned.
        :return: Parse with the longest root word.
        """
        maxLength = -1
        bestParse = None
        for currentParse in self.__fsmParses:
            if len(currentParse.getWord().getName()) > maxLength and not self.isLongestRootException(currentParse):
                maxLength = len(currentParse.getWord().getName())
                bestParse = currentParse
        return bestParse

    def isLongestRootException(self, fsmParse: FsmParse) -> bool:
        """
        The isLongestRootException method returns true if the longest root word belongs to an exceptional case, false
        otherwise.
        :param fsmParse: FsmParse input
        :return: true if the longest root belongs to an exceptional case, false otherwise.
        """
        surfaceForm = fsmParse.getSurfaceForm()
        root = fsmParse.getWord().getName()
        for longestRootException in self.longestRootExceptions:
            exceptionItems = longestRootException.split(" ")
            surfaceFormEnding = exceptionItems[0]
            longestRootEnding = exceptionItems[1]
            longestRootPos = exceptionItems[2]
            possibleRootPos = exceptionItems[3]
            possibleRoot = surfaceForm.replace(surfaceFormEnding, "")
            if surfaceForm.endswith(surfaceFormEnding) and root.endswith(longestRootEnding) \
                    and fsmParse.getRootPos() == longestRootPos:
                for currentParse in self.__fsmParses:
                    if currentParse.getWord().getName() == possibleRoot \
                            and currentParse.getRootPos() == possibleRootPos:
                        return True
        return False

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
