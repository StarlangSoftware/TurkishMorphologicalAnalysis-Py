from Dictionary.TxtWord import TxtWord
from Dictionary.Word import Word

from MorphologicalAnalysis.InflectionalGroup import InflectionalGroup
from MorphologicalAnalysis.MorphologicalParse import MorphologicalParse
from MorphologicalAnalysis.State import State


class FsmParse(MorphologicalParse):
    __suffixList: list
    __formList: list
    __transitionList: list
    __withList: list
    __initialPos: str
    __pos: str
    __form: str
    __verbAgreement: str
    __possesiveAgreement: str

    def __init__(self, root, startState=None):
        """
        Another constructor of FsmParse class which takes a TxtWord root and a State as inputs.
        First, initializes root variable with this TxtWord. It also initializes form with root's name, pos and
        initialPos with given State's POS, creates 4 new list suffixList, formList, transitionList
        and withList and adds given State to suffixList, form to formList.

        PARAMETERS
        ----------
        root : TxtWord
            TxtWord input.
        startState : State
            State input.
        """
        if isinstance(root, Word):
            self.root = root
        elif isinstance(root, int):
            self.root = TxtWord(str(root))
            self.root.addFlag("IS_SAYI")
        elif isinstance(root, float):
            self.root = TxtWord(str(root))
            self.root.addFlag("IS_SAYI")
        elif isinstance(root, str):
            self.root = TxtWord(root)
        if startState is not None:
            self.__form = self.root.getName()
            self.__pos = startState.getPos()
            self.__initialPos = startState.getPos()
            self.__suffixList = []
            self.__suffixList.append(startState)
            self.__formList = []
            self.__formList.append(self.__form)
            self.__transitionList = []
            self.__withList = []
        self.__verbAgreement = None
        self.__possesiveAgreement = None

    def __eq__(self, other):
        return self.transitionList() == other.transitionList()

    def __lt__(self, other):
        return self.transitionList() < other.transitionList()

    def __gt__(self, other):
        return self.transitionList() > other.transitionList()

    def constructInflectionalGroups(self):
        """
        The constructInflectionalGroups method initially calls the transitionList method and assigns the resulting str
        to the parse variable and creates a new list as iGs. If parse str contains a derivational boundary
        it adds the substring starting from the 0 to the index of derivational boundary to the iGs. If it does not
        contain a DB, it directly adds parse to the iGs. Then, creates and initializes new list as inflectionalGroups
        and fills with the items of iGs.
        """
        parse = self.transitionList()
        iGs = []
        while "^DB+" in parse:
            iGs.append(parse[:parse.index("^DB+")])
            parse = parse[parse.index("^DB+") + 4:]
        iGs.append(parse)
        self.inflectionalGroups = []
        self.inflectionalGroups.append(InflectionalGroup(iGs[0][iGs[0].index("+") + 1:]))
        for i in range(1, len(iGs)):
            self.inflectionalGroups.append(InflectionalGroup(iGs[i]))

    def getVerbAgreement(self) -> str:
        """
        Getter for the verbAgreement variable.

        RETURNS
        -------
        str
            The verbAgreement variable.
        """
        return self.__verbAgreement

    def getPossesiveAgreement(self) -> str:
        """
        Getter for the possesiveAgreement variable.

        RETURNS
        -------
        str
            The possesiveAgreement variable.
        """
        return self.__possesiveAgreement

    def setAgreement(self, transitionName: str):
        """
        The setAgreement method takes a str transitionName as an input and if it is one of the A1SG, A2SG, A3SG,
        A1PL, A2PL or A3PL it assigns transitionName input to the verbAgreement variable. Or if it is ine of the PNON,
        P1SG, P2SG,P3SG, P1PL, P2PL or P3PL it assigns transitionName input to the possesiveAgreement variable.

        PARAMETERS
        ----------
        transitionName : str
            String input.
        """
        if transitionName == "A1SG" or transitionName == "A2SG" or transitionName == "A3SG" or transitionName == "A1PL"\
                or transitionName == "A2PL" or transitionName == "A3PL":
            self.__verbAgreement = transitionName
        if transitionName == "PNON" or transitionName == "P1SG" or transitionName == "P2SG" or transitionName == "P3SG"\
                or transitionName == "P1PL" or transitionName == "P2PL" or transitionName == "P3PL":
            self.__possesiveAgreement = transitionName

    def getLastLemmaWithTag(self, pos: str) -> str:
        """
        The getLastLemmaWithTag method takes a String input pos as an input. If given pos is an initial pos then it
        assigns root to the lemma, and assign null otherwise. Then, it loops i times where i ranges from 1 to size of
        the formList, if the item at i-1 of transitionList is not null and contains a derivational boundary with pos but
        not with ZERO, it assigns the ith item of formList to lemma.

        PARAMETERS
        ----------
        pos : str
            String input.

        RETURNS
        -------
        str
            String output lemma.
        """
        if self.__initialPos is not None and self.__initialPos == pos:
            lemma = self.root.getName()
        else:
            lemma = None
        for i in range(1, len(self.__formList)):
            if self.__transitionList[i - 1] is not None and ("^DB+" + pos) in self.__transitionList[i - 1] and \
                    ("^DB+" + pos + "+ZERO") not in self.__transitionList[i - 1]:
                lemma = self.__formList[i]
        return lemma

    def getLastLemma(self) -> str:
        """
        The getLastLemma method initially assigns root as lemma. Then, it loops i times where i ranges from 1 to size of
        the formList, if the item at i-1 of transitionList is not null and contains a derivational boundary, it assigns
        the ith item of formList to lemma.

        RETURNS
        -------
        str
            String output lemma.
        """
        lemma = self.root.getName()
        for i in range(1, len(self.__formList)):
            if self.__transitionList[i - 1] is not None and "^DB+" in self.__transitionList[i - 1]:
                lemma = self.__formList[i]
        return lemma

    def addSuffix(self, suffix: State, form: str, transition: str, withName: str, toPos: str):
        """
        The addSuffix method takes 5 different inputs; State suffix, str form, transition, with and toPos.
        If the pos of given input suffix is not None, it then assigns it to the pos variable. If the pos of the given
        suffix is None but given toPos is not None than it assigns toPos to pos variable. At the end, it adds suffix to
        the suffixList, form to the formList, transition to the transitionList and if given with is not 0, it is also
        added to withList.

        PARAMETERS
        ----------
        suffix : State
            State input.
        form : str
            String input.
        transition : str
            String input.
        withName : str
            String input.
        toPos : str
            String input.
        """
        if suffix.getPos() is not None:
            self.__pos = suffix.getPos()
        else:
            if toPos is not None:
                self.__pos = toPos
        self.__suffixList.append(suffix)
        self.__formList.append(form)
        self.__transitionList.append(transition)
        if withName != "0":
            self.__withList.append(withName)
        self.__form = form

    def getSurfaceForm(self) -> str:
        """
        Getter for the form variable.

        RETURNS
        -------
        str
            The form variable.
        """
        return self.__form

    def getStartState(self) -> State:
        """
        The getStartState method returns the first item of suffixList list.

        RETURNS
        -------
        State
            The first item of suffixList list.
        """
        return self.__suffixList[0]

    def getFinalPos(self) -> str:
        """
        Getter for the pos variable.

        RETURNS
        -------
        str
            The pos variable.
        """
        return self.__pos

    def getInitialPos(self) -> str:
        """
        Getter for the initialPos variable.

        RETURNS
        -------
        str
            The initialPos variable.
        """
        return self.__initialPos

    def setForm(self, name: str):
        """
        The setForm method takes a str name as an input and assigns it to the form variable, then it removes the first
        item of formList list and adds the given name to the formList.

        PARAMETERS
        ----------
        name : str
            String input to set form.
        """
        self.__form = name
        self.__formList.pop(0)
        self.__formList.append(name)

    def getFinalSuffix(self) -> State:
        """
        The getFinalSuffix method returns the last item of suffixList list.

        RETURNS
        -------
        State
            The last item of suffixList list.
        """
        return self.__suffixList[len(self.__suffixList) - 1]

    def headerTransition(self) -> str:
        """
        The headerTransition method gets the first item of formList and checks for cases;

        If it is <DOC>, it returns "<DOC>+BDTAG" which indicates the beginning of a document.
        If it is </DOC>, it returns "</DOC>+EDTAG" which indicates the ending of a document.
        If it is <TITLE>, it returns "<TITLE>+BTTAG" which indicates the beginning of a title.
        If it is </TITLE>, it returns "</TITLE>+ETTAG" which indicates the ending of a title.
        If it is "<S>", it returns "<S>+BSTAG" which indicates the beginning of a sentence.
        If it is "</S>, it returns "</S>+ESTAG" which indicates the ending of a sentence.

        RETURNS
        -------
        str
            Corresponding tags of the headers and an empty {@link String} if any case does not match.
        """
        if self.__formList[0] == "<DOC>":
            return "<DOC>+BDTAG"
        elif self.__formList[0] == "</DOC>":
            return "</DOC>+EDTAG"
        elif self.__formList[0] == "<TITLE>":
            return "<TITLE>+BTTAG"
        elif self.__formList[0] == "</TITLE>":
            return "</TITLE>+ETTAG"
        elif self.__formList[0] == "<S>":
            return "<S>+BSTAG"
        elif self.__formList[0] == "</S>":
            return "</S>+ESTAG"
        else:
            return ""

    def pronounTransition(self) -> str:
        """
        The pronounTransition method gets the first item of formList and checks for cases;

        If it is "kendi", it returns kendi+PRON+REFLEXP which indicates a reflexive pronoun.
        If it is one of the "hep, öbür, topu, öteki, kimse, hiçbiri, tümü, çoğu, hepsi, herkes, başkası, birçoğu,
        birçokları, biri, birbirleri, birbiri, birkaçı, böylesi, diğeri, cümlesi, bazı, kimi", it returns
        +PRON+QUANTP which indicates a quantitative pronoun.
        If it is one of the "o, bu, şu" and if it is "o" it also checks the first item of suffixList and if it is a
        PronounRoot(DEMONS), it returns +PRON+DEMONSP which indicates a demonstrative pronoun.
        If it is "ben", it returns +PRON+PERS+A1SG+PNON which indicates a 1st person singular agreement.
        If it is "sen", it returns +PRON+PERS+A2SG+PNON which indicates a 2nd person singular agreement.
        If it is "o" and the first item of suffixList, if it is a PronounRoot(PERS), it returns +PRON+PERS+A3SG+PNON
        which indicates a 3rd person singular agreement.
        If it is "biz", it returns +PRON+PERS+A1PL+PNON which indicates a 1st person plural agreement.
        If it is "siz", it returns +PRON+PERS+A2PL+PNON which indicates a 2nd person plural agreement.
        If it is "onlar" and the first item of suffixList, if it is a PronounRoot(PERS), it returns
        o+PRON+PERS+A3PL+PNON which indicates a 3rd person plural agreement.
        If it is one of the "nere, ne, kim, hangi", it returns +PRON+QUESP which indicates a question pronoun.

        RETURNS
        -------
        str
            Corresponding transitions of pronouns and an empty str if any case does not match.
        """
        if self.__formList[0] == "kendi":
            return "kendi+PRON+REFLEXP"
        elif self.__formList[0] == "hep" or self.__formList[0] == "öbür" or self.__formList[0] == "topu" \
                or self.__formList[0] == "öteki" or self.__formList[0] == "kimse" or self.__formList[0] == "hiçbiri" \
                or self.__formList[0] == "tümü" or self.__formList[0] == "çoğu" or self.__formList[0] == "hepsi" \
                or self.__formList[0] == "herkes" or self.__formList[0] == "başkası" or self.__formList[0] == "birçoğu"\
                or self.__formList[0] == "birçokları" or self.__formList[0] == "birbiri" \
                or self.__formList[0] == "birbirleri" or self.__formList[0] == "biri" \
                or self.__formList[0] == "birkaçı" or self.__formList[0] == "böylesi" or self.__formList[0] == "diğeri"\
                or self.__formList[0] == "cümlesi" or self.__formList[0] == "bazı" or self.__formList[0] == "kimi":
            return self.__formList[0] + "+PRON+QUANTP"
        elif (self.__formList[0] == "o" and self.__suffixList[0].getName() == "PronounRoot(DEMONS)") \
                or self.__formList[0] == "bu" or self.__formList[0] == "şu":
            return self.__formList[0] + "+PRON+DEMONSP"
        elif self.__formList[0] == "ben":
            return self.__formList[0] + "+PRON+PERS+A1SG+PNON"
        elif self.__formList[0] == "sen":
            return self.__formList[0] + "+PRON+PERS+A2SG+PNON"
        elif self.__formList[0] == "o" and self.__suffixList[0].getName() == "PronounRoot(PERS)":
            return self.__formList[0] + "+PRON+PERS+A3SG+PNON"
        elif self.__formList[0] == "biz":
            return self.__formList[0] + "+PRON+PERS+A1PL+PNON"
        elif self.__formList[0] == "siz":
            return self.__formList[0] + "+PRON+PERS+A2PL+PNON"
        elif self.__formList[0] == "onlar":
            return "o+PRON+PERS+A3PL+PNON"
        elif self.__formList[0] == "nere" or self.__formList[0] == "ne" or self.__formList[0] == "kaçı" \
                or self.__formList[0] == "kim" or self.__formList[0] == "hangi":
            return self.__formList[0] + "+PRON+QUESP"
        else:
            return ""

    def transitionList(self) -> str:
        """
        The transitionList method first creates an empty {@link String} result, then gets the first item of suffixList
        and checks for cases; If it is one of the "NominalRoot, NominalRootNoPossesive, CompoundNounRoot,
        NominalRootPlural", it assigns concatenation of first item of formList and +NOUN to the result String.
        Ex : Birincilik

        If it is one of the "VerbalRoot, PassiveHn", it assigns concatenation of first item of formList and +VERB to the
        result String.
        Ex : Başkalaştı

        If it is "CardinalRoot", it assigns concatenation of first item of formList and +NUM+CARD to the result String.
        Ex : Onuncu

        If it is "FractionRoot", it assigns concatenation of first item of formList and NUM+FRACTION to the result
        String.
        Ex : 1/2

        If it is "TimeRoot", it assigns concatenation of first item of formList and +TIME to the result String.
        Ex : 14:28

        If it is "RealRoot", it assigns concatenation of first item of formList and +NUM+REAL to the result String.
        Ex : 1.2

        If it is "Punctuation", it assigns concatenation of first item of formList and +PUNC to the result String.
        Ex : ,

        If it is "Hashtag", it assigns concatenation of first item of formList and +HASHTAG to the result String.
        Ex : #

        If it is "DateRoot", it assigns concatenation of first item of formList and +DATE to the result String.
        Ex : 11/06/2018

        If it is "RangeRoot", it assigns concatenation of first item of formList and +RANGE to the result String.
        Ex : 3-5

        If it is "Email", it assigns concatenation of first item of formList and +EMAIL to the result String.
        Ex : abc@

        If it is "PercentRoot", it assigns concatenation of first item of formList and +PERCENT to the result String.
        Ex : %12.5

        If it is "DeterminerRoot", it assigns concatenation of first item of formList and +DET to the result String.
        Ex : Birtakım

        If it is "ConjunctionRoot", it assigns concatenation of first item of formList and +CONJ to the result String.
        Ex : Ama

        If it is "AdverbRoot", it assigns concatenation of first item of formList and +ADV to the result String.
        Ex : Acilen

        If it is "ProperRoot", it assigns concatenation of first item of formList and +NOUN+PROP to the result String.
        Ex : Ahmet

        If it is "HeaderRoot", it assigns the result of the headerTransition method to the result String.
        Ex : &lt;DOC&gt;

        If it is "InterjectionRoot", it assigns concatenation of first item of formList and +INTERJ to the result
        String.
        Ex : Hey

        If it is "DuplicateRoot", it assigns concatenation of first item of formList and +DUP to the result String.
        Ex : Allak

        If it is "QuestionRoot", it assigns concatenation of first item of formList and +QUES to the result String.
        Ex : Mı

        If it is "PostP", and the first item of formList is one of the "karşı, ilişkin, göre, kadar, ait, yönelik,
        rağmen, değin, dek, doğru, karşın, dair, atfen, binaen, hitaben, istinaden, mahsuben, mukabil, nazaran", it
        assigns concatenation of first item of formList and +POSTP+PCDAT to the result String.
        Ex : İlişkin

        If it is "PostP", and the first item of formList is one of the "sonra, önce, beri, fazla, dolayı, itibaren,
        başka, çok, evvel, ötürü, yana, öte, aşağı, yukarı, dışarı, az, gayrı", it assigns concatenation of first
        item of formList and +POSTP+PCABL to the result String.
        Ex : Başka

        If it is "PostP", and the first item of formList is "yanısıra", it assigns concatenation of first
        item of formList and +POSTP+PCGEN to the result String.
        Ex : Yanısıra

        If it is "PostP", and the first item of formList is one of the "birlikte, beraber", it assigns concatenation of
        first item of formList and +PPOSTP+PCINS to the result String.
        Ex : Birlikte

        If it is "PostP", and the first item of formList is one of the "aşkın, takiben", it assigns concatenation of
        first item of formList and +POSTP+PCACC to the result String.
        Ex : Takiben

        If it is "PostP", it assigns concatenation of first item of formList and +POSTP+PCNOM to the result String.

        If it is "PronounRoot", it assigns result of the pronounTransition method to the result String.
        Ex : Ben

        If it is "OrdinalRoot", it assigns concatenation of first item of formList and +NUM+ORD to the result String.
        Ex : Altıncı

        If it starts with "Adjective", it assigns concatenation of first item of formList and +ADJ to the result String.
        Ex : Güzel

        At the end, it loops through the formList and concatenates each item with result {@link String}.

        RETURNS
        -------
        str
            str result accumulated with items of formList.
        """
        result = ""
        if self.__suffixList[0].getName() == "NominalRoot" \
                or self.__suffixList[0].getName() == "NominalRootNoPossesive" \
                or self.__suffixList[0].getName() == "CompoundNounRoot" \
                or self.__suffixList[0].getName() == "NominalRootPlural":
            result = self.__formList[0] + "+NOUN"
        elif self.__suffixList[0].getName().startswith("VerbalRoot") or self.__suffixList[0].getName() == "PassiveHn":
            result = self.__formList[0] + "+VERB"
        elif self.__suffixList[0].getName() == "CardinalRoot":
            result = self.__formList[0] + "+NUM+CARD"
        elif self.__suffixList[0].getName() == "FractionRoot":
            result = self.__formList[0] + "+NUM+FRACTION"
        elif self.__suffixList[0].getName() == "TimeRoot":
            result = self.__formList[0] + "+TIME"
        elif self.__suffixList[0].getName() == "RealRoot":
            result = self.__formList[0] + "+NUM+REAL"
        elif self.__suffixList[0].getName() == "Punctuation":
            result = self.__formList[0] + "+PUNC"
        elif self.__suffixList[0].getName() == "Hashtag":
            result = self.__formList[0] + "+HASHTAG"
        elif self.__suffixList[0].getName() == "DateRoot":
            result = self.__formList[0] + "+DATE"
        elif self.__suffixList[0].getName() == "RangeRoot":
            result = self.__formList[0] + "+RANGE"
        elif self.__suffixList[0].getName() == "Email":
            result = self.__formList[0] + "+EMAIL"
        elif self.__suffixList[0].getName() == "PercentRoot":
            result = self.__formList[0] + "+PERCENT"
        elif self.__suffixList[0].getName() == "DeterminerRoot":
            result = self.__formList[0] + "+DET"
        elif self.__suffixList[0].getName() == "ConjunctionRoot":
            result = self.__formList[0] + "+CONJ"
        elif self.__suffixList[0].getName() == "AdverbRoot":
            result = self.__formList[0] + "+ADV"
        elif self.__suffixList[0].getName() == "ProperRoot":
            result = self.__formList[0] + "+NOUN+PROP"
        elif self.__suffixList[0].getName() == "HeaderRoot":
            result = self.headerTransition()
        elif self.__suffixList[0].getName() == "InterjectionRoot":
            result = self.__formList[0] + "+INTERJ"
        elif self.__suffixList[0].getName() == "DuplicateRoot":
            result = self.__formList[0] + "+DUP"
        elif self.__suffixList[0].getName() == "QuestionRoot":
            result = self.__formList[0] + "+QUES"
        elif self.__suffixList[0].getName() == "PostP":
            if self.__formList[0] == "karşı" or self.__formList[0] == "ilişkin" or self.__formList[0] == "göre" \
                    or self.__formList[0] == "kadar" or self.__formList[0] == "ait" or self.__formList[0] == "yönelik" \
                    or self.__formList[0] == "rağmen" or self.__formList[0] == "değin" or self.__formList[0] == "dek" \
                    or self.__formList[0] == "doğru" or self.__formList[0] == "karşın" or self.__formList[0] == "dair" \
                    or self.__formList[0] == "atfen" or self.__formList[0] == "binaen" or self.__formList[
                0] == "hitaben" \
                    or self.__formList[0] == "istinaden" or self.__formList[0] == "mahsuben" \
                    or self.__formList[0] == "mukabil" or self.__formList[0] == "nazaran":
                result = self.__formList[0] + "+POSTP+PCDAT"
            elif self.__formList[0] == "sonra" or self.__formList[0] == "önce" or self.__formList[0] == "beri" \
                    or self.__formList[0] == "fazla" or self.__formList[0] == "dolayı" or self.__formList[
                0] == "itibaren" \
                    or self.__formList[0] == "başka" or self.__formList[0] == "çok" or self.__formList[0] == "evvel" \
                    or self.__formList[0] == "ötürü" or self.__formList[0] == "yana" or self.__formList[0] == "öte" \
                    or self.__formList[0] == "aşağı" or self.__formList[0] == "yukarı" \
                    or self.__formList[0] == "dışarı" or self.__formList[0] == "az" or self.__formList[0] == "gayrı":
                result = self.__formList[0] + "+POSTP+PCABL"
            elif self.__formList[0] == "yanısıra":
                result = self.__formList[0] + "+POSTP+PCGEN"
            elif self.__formList[0] == "birlikte" or self.__formList[0] == "beraber":
                result = self.__formList[0] + "+POSTP+PCINS"
            elif self.__formList[0] == "aşkın" or self.__formList[0] == "takiben":
                result = self.__formList[0] + "+POSTP+PCACC"
            else:
                result = self.__formList[0] + "+POSTP+PCNOM"
        elif self.__suffixList[0].getName().startswith("PronounRoot"):
            result = self.pronounTransition()
        elif self.__suffixList[0].getName() == "OrdinalRoot":
            result = self.__formList[0] + "+NUM+ORD"
        elif self.__suffixList[0].getName().startswith("Adjective"):
            result = self.__formList[0] + "+ADJ"
        for transition in self.__transitionList:
            if transition is not None:
                if not transition.startswith("^"):
                    result = result + "+" + transition
                else:
                    result = result + transition
        return result

    def suffixList(self) -> str:
        """
        The suffixList method gets the first items of suffixList and formList and concatenates them with parenthesis and
        assigns a String result. Then, loops through the formList and it the current ith item is not equal to previous
        item it accumulates ith items of formList and suffixList to the result str.

        RETURNS
        -------
        str
            result str accumulated with the items of formList and suffixList.
        """
        result = self.__suffixList[0].getName() + "(" + self.__formList[0] + ")"
        for i in range(1, len(self.__formList)):
            if self.__formList[i] != self.__formList[i - 1]:
                result = result + "+" + self.__suffixList[i].getName() + "(" + self.__formList[i] + ")"
        return result

    def withList(self) -> str:
        """
        The withList method gets the root as a result str then loops through the withList and concatenates each item
        with result str.

        RETURNS
        -------
        str
            result str accumulated with items of withList.
        """
        result = self.root.getName()
        for aWith in self.__withList:
            result = result + "+" + aWith
        return result

    def __str__(self) -> str:
        """
        The overridden str method which returns transitionList method.

        RETURNS
        -------
        str
            Returns transitionList method.
        """
        return self.transitionList()
