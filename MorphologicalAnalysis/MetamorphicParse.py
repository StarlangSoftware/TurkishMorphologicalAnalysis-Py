from Dictionary.Word import Word

from MorphologicalAnalysis.MorphologicalParse import MorphologicalParse
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag


class MetamorphicParse:

    """
    MetaMorphemes that can be used.
    """
    metaMorphemes = ["Ar", "Ar", "CA", "CA",
                     "CA", "cAsHnA", "CH", "CHk",
                     "DA", "DAn", "DH", "DHk",
                     "DHkCA", "DHr", "DHr", "DHr",
                     "H", "Hl", "Hm", "Hn",
                     "Hn", "Hn", "HmHz", "HncH",
                     "HnHz", "Hr", "Hr", "Hs",
                     "Ht", "Hyor", "Hz", "k",
                     "ki", "kü", "lAn", "lAr",
                     "lArDHr", "lArH", "lArH'", "lAs",
                     "lH", "lHk", "lHm", "m",
                     "mA", "mA", "mAcA", "mAdAn",
                     "mAk", "mAksHzHn", "mAktA", "mAlH",
                     "mAzlHk", "mHs", "n", "n",
                     "nA", "ncA", "nDA", "nDAn",
                     "nH", "nHn", "nHz", "nlAr",
                     "SA", "SAl", "sH", "SH",
                     "SH", "SHn", "SHnHz", "SHnlAr",
                     "SHz", "ŞAr", "t", "yA",
                     "yA", "yAbil", "yAcAk", "yAcAk",
                     "yAdur", "yAgel", "yAlH", "yAmA",
                     "yAmAdAn", "yAn", "yArAk", "yAsH",
                     "yDH", "yH", "yHcH", "yHm",
                     "yHn", "yHncA", "yHp", "yHs",
                     "yHver", "yHz", "yken", "ylA",
                     "ymHs", "ysA", "z", "zsHn",
                     "zsHnHz", "zlAr", "yAkal", "yAkoy",
                     "yAgor"]

    """
    MorphotacticTags that can be used.
    """
    morphotacticTags = [
        MorphologicalTag.AORIST,
        MorphologicalTag.CAUSATIVE,
        MorphologicalTag.ASIF,
        MorphologicalTag.LY,
        MorphologicalTag.EQUATIVE,
        MorphologicalTag.ASIF,
        MorphologicalTag.AGENT,
        MorphologicalTag.DIMENSION,
        MorphologicalTag.LOCATIVE,
        MorphologicalTag.ABLATIVE,
        MorphologicalTag.PASTTENSE,
        MorphologicalTag.PASTPARTICIPLE,
        MorphologicalTag.ASLONGAS,
        MorphologicalTag.COPULA,
        MorphologicalTag.SINCE,
        MorphologicalTag.CAUSATIVE,
        MorphologicalTag.P3SG,
        MorphologicalTag.PASSIVE,
        MorphologicalTag.P1SG,
        MorphologicalTag.REFLEXIVE,
        MorphologicalTag.PASSIVE,
        MorphologicalTag.P2SG,
        MorphologicalTag.P1PL,
        MorphologicalTag.ORDINAL,
        MorphologicalTag.P2PL,
        MorphologicalTag.AORIST,
        MorphologicalTag.CAUSATIVE,
        MorphologicalTag.RECIPROCAL,
        MorphologicalTag.CAUSATIVE,
        MorphologicalTag.PROGRESSIVE1,
        MorphologicalTag.A1PL,
        MorphologicalTag.A1PL,
        MorphologicalTag.RELATIVE,
        MorphologicalTag.RELATIVE,
        MorphologicalTag.ACQUIRE,
        MorphologicalTag.A3PL,
        MorphologicalTag.SINCE,
        MorphologicalTag.P3PL,
        MorphologicalTag.P3PL,
        MorphologicalTag.BECOME,
        MorphologicalTag.WITH,
        MorphologicalTag.NESS,
        MorphologicalTag.A1PL,
        MorphologicalTag.A1SG,
        MorphologicalTag.INFINITIVE2,
        MorphologicalTag.NEGATIVE,
        MorphologicalTag.ACTOF,
        MorphologicalTag.WITHOUTHAVINGDONESO,
        MorphologicalTag.INFINITIVE,
        MorphologicalTag.WITHOUTHAVINGDONESO,
        MorphologicalTag.PROGRESSIVE2,
        MorphologicalTag.NECESSITY,
        MorphologicalTag.NOTABLESTATE,
        MorphologicalTag.NARRATIVE,
        MorphologicalTag.A2SG,
        MorphologicalTag.PASSIVE,
        MorphologicalTag.DATIVE,
        MorphologicalTag.EQUATIVE,
        MorphologicalTag.LOCATIVE,
        MorphologicalTag.ABLATIVE,
        MorphologicalTag.ACCUSATIVE,
        MorphologicalTag.GENITIVE,
        MorphologicalTag.A2PL,
        MorphologicalTag.A3PL,
        MorphologicalTag.DESIRE,
        MorphologicalTag.RELATED,
        MorphologicalTag.P3SG,
        MorphologicalTag.JUSTLIKE,
        MorphologicalTag.ALMOST,
        MorphologicalTag.A2SG,
        MorphologicalTag.A2PL,
        MorphologicalTag.A3PL,
        MorphologicalTag.WITHOUT,
        MorphologicalTag.DISTRIBUTIVE,
        MorphologicalTag.CAUSATIVE,
        MorphologicalTag.DATIVE,
        MorphologicalTag.OPTATIVE,
        MorphologicalTag.ABLE,
        MorphologicalTag.FUTUREPARTICIPLE,
        MorphologicalTag.FUTURE,
        MorphologicalTag.REPEAT,
        MorphologicalTag.EVERSINCE,
        MorphologicalTag.SINCEDOINGSO,
        MorphologicalTag.NOTABLESTATE,
        MorphologicalTag.WITHOUTBEINGABLETOHAVEDONESO,
        MorphologicalTag.PRESENTPARTICIPLE,
        MorphologicalTag.BYDOINGSO,
        MorphologicalTag.FEELLIKE,
        MorphologicalTag.PASTTENSE,
        MorphologicalTag.ACCUSATIVE,
        MorphologicalTag.AGENT,
        MorphologicalTag.A1SG,
        MorphologicalTag.A2PL,
        MorphologicalTag.WHEN,
        MorphologicalTag.AFTERDOINGSO,
        MorphologicalTag.INFINITIVE3,
        MorphologicalTag.HASTILY,
        MorphologicalTag.A1PL,
        MorphologicalTag.WHILE,
        MorphologicalTag.INSTRUMENTAL,
        MorphologicalTag.NARRATIVE,
        MorphologicalTag.CONDITIONAL,
        MorphologicalTag.A3SG,
        MorphologicalTag.A2SG,
        MorphologicalTag.A2PL,
        MorphologicalTag.A3PL,
        MorphologicalTag.STAY,
        MorphologicalTag.START,
        MorphologicalTag.REPEAT]

    __metaMorphemeList: list
    __root: Word

    def __init__(self, parse=None):
        """
        A constructor of MetamorphicParse class which creates an list metaMorphemeList which has split words
        according to +.

        PARAMETERS
        ----------
        parse : str
            String to parse.
        """
        if parse is not None:
            self.__metaMorphemeList = []
            if parse == "+":
                self.__root = Word("+")
            else:
                words = parse.split("\\+")
                self.__root = Word(words[0])
                for i in range(1, len(words)):
                    self.__metaMorphemeList.append(words[i])

    def getMetaMorphemeTag(self, tag: str) -> list:
        """
        The getMetaMorphemeTag method takes a String tag as an input and takes the first char of the tag. If first char
        is a punctuation it gets a substring from the tag. And gets the meta morphemes of this tag then adds to the
        result list.

        PARAMETERS
        ----------
        tag : str
            String to get meta morphemes from.

        RETURNS
        -------
        list
            List type result which holds meta morphemes.
        """
        result = []
        s = tag[0]
        if Word.isPunctuationSymbol(s):
            tag = tag[1:]
        for j in range(len(MetamorphicParse.metaMorphemes)):
            if tag == self.metaMorphemes[j]:
                result.append(MetamorphicParse.morphotacticTags[j])
        return result

    def getWord(self) -> Word:
        """
        The getter method for Private Word root.

        RETURNS
        -------
        Word
            Word type root.
        """
        return self.__root

    def getMetaMorphemeTagForParse(self, parse: MorphologicalParse, tag: str) -> list:
        """
        getMetaMorphemeTagForParse method which also takes parse as an input. It also checks the morphotactic tags.

        PARAMETERS
        ----------
        parse : MorphologicalParse
            MorphologicalParse type input.
        tag : str
            String to get meta morphemes from.

        RETURNS
        -------
        list
            List type result which holds meta morphemes.
        """
        result = []
        s = tag[0]
        if Word.isPunctuationSymbol(s):
            tag = tag[1:]
        for j in range(len(MetamorphicParse.metaMorphemes)):
            if tag == self.metaMorphemes[j] and parse.containsTag(MetamorphicParse.morphotacticTags[j]):
                result.append(MetamorphicParse.morphotacticTags[j])
        return result

    def size(self) -> int:
        """
        The size method returns the size of the metaMorphemeList.

        RETURNS
        -------
        int
            The size of the metaMorphemeList.
        """
        return len(self.__metaMorphemeList) + 1

    def addMetaMorphemeList(self, newTacticSet: str):
        """
        The addMetaMorphemeList method splits input String by + and add to the metaMorphemeList.

        PARAMETERS
        ----------
        newTacticSet : str
            String to add the metaMorphemeList.
        """
        tactics = newTacticSet.split("\\+")
        self.__metaMorphemeList.extend(tactics)

    def removeMetaMorphemeFromIndex(self, index: int):
        """
        The removeMetaMorphemeFromIndex method removes the meta morpheme at given index from metaMorphemeList.

        PARAMETERS
        ----------
        index : int
            to remove from metaMorphemeList.
        """
        i = index - 1
        while i < len(self.__metaMorphemeList):
            self.__metaMorphemeList.pop(i)

    def getMetaMorpheme(self, index: int) -> str:
        """
        The getMetaMorpheme method gets the meta morpheme at given index.

        PARAMETERS
        ----------
        index : int
            is used to get the meta morpheme.

        RETURNS
        -------
        str
            metaMorphemeList's corresponding meta morpheme.
        """
        if index == 0:
            return self.__root.getName()
        else:
            return self.__metaMorphemeList[index - 1]

    def __str__(self) -> str:
        """
        Overridden __str__ method to return resulting meta morphemes in metaMorphemeList.

        RETURNS
        -------
        str
            String result.
        """
        result = self.__root.getName()
        for metaMorpheme in self.__metaMorphemeList:
            result = result + "+" + metaMorpheme
        return result
