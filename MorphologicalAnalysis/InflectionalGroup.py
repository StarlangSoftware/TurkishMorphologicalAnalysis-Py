from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag


class InflectionalGroup:
    __IG: list
    tags = ["NOUN", "ADV", "ADJ", "VERB", "A1SG",
            "A2SG", "A3SG", "A1PL", "A2PL", "A3PL",
            "P1SG", "P2SG", "P3SG", "P1PL", "P2PL",
            "P3PL", "PROP", "PNON", "NOM", "WITH",
            "WITHOUT", "ACC", "DAT", "GEN", "ABL",
            "ZERO", "ABLE", "NEG", "PAST",
            "CONJ", "DET", "DUP", "INTERJ", "NUM",
            "POSTP", "PUNC", "QUES", "AGT", "BYDOINGSO",
            "CARD", "CAUS", "DEMONSP", "DISTRIB", "FITFOR",
            "FUTPART", "INF", "NESS", "ORD", "PASS",
            "PASTPART", "PRESPART", "QUESP", "QUANTP", "RANGE",
            "RATIO", "REAL", "RECIP", "REFLEX", "REFLEXP",
            "TIME", "WHEN", "WHILE", "WITHOUTHAVINGDONESO", "PCABL",
            "PCACC", "PCDAT", "PCGEN", "PCINS", "PCNOM",
            "ACQUIRE", "ACTOF", "AFTERDOINGSO", "ALMOST", "AS",
            "ASIF", "BECOME", "EVERSINCE", "FEELLIKE", "HASTILY",
            "INBETWEEN", "JUSTLIKE", "LY", "NOTABLESTATE", "RELATED",
            "REPEAT", "SINCE", "SINCEDOINGSO", "START", "STAY",
            "EQU", "INS", "AOR", "DESR", "FUT",
            "IMP", "NARR", "NECES", "OPT", "PAST",
            "PRES", "PROG1", "PROG2", "COND", "COP",
            "POS", "PRON", "LOC", "REL", "DEMONS",
            "INF2", "INF3", "BSTAG", "ESTAG", "BTTAG",
            "ETTAG", "BDTAG", "EDTAG", "INF1", "ASLONGAS",
            "DIST", "ADAMANTLY", "PERCENT", "WITHOUTBEINGABLETOHAVEDONESO", "DIM",
            "PERS", "FRACTION", "HASHTAG", "EMAIL", "DATE"]
    morphotags = [MorphologicalTag.NOUN, MorphologicalTag.ADVERB, MorphologicalTag.ADJECTIVE,
                  MorphologicalTag.VERB, MorphologicalTag.A1SG, MorphologicalTag.A2SG, MorphologicalTag.A3SG,
                  MorphologicalTag.A1PL,
                  MorphologicalTag.A2PL, MorphologicalTag.A3PL, MorphologicalTag.P1SG, MorphologicalTag.P2SG,
                  MorphologicalTag.P3SG, MorphologicalTag.P1PL,
                  MorphologicalTag.P2PL, MorphologicalTag.P3PL, MorphologicalTag.PROPERNOUN, MorphologicalTag.PNON,
                  MorphologicalTag.NOMINATIVE,
                  MorphologicalTag.WITH, MorphologicalTag.WITHOUT, MorphologicalTag.ACCUSATIVE, MorphologicalTag.DATIVE,
                  MorphologicalTag.GENITIVE,
                  MorphologicalTag.ABLATIVE, MorphologicalTag.ZERO, MorphologicalTag.ABLE, MorphologicalTag.NEGATIVE,
                  MorphologicalTag.PASTTENSE,
                  MorphologicalTag.CONJUNCTION, MorphologicalTag.DETERMINER, MorphologicalTag.DUPLICATION,
                  MorphologicalTag.INTERJECTION, MorphologicalTag.NUMBER,
                  MorphologicalTag.POSTPOSITION, MorphologicalTag.PUNCTUATION, MorphologicalTag.QUESTION,
                  MorphologicalTag.AGENT, MorphologicalTag.BYDOINGSO,
                  MorphologicalTag.CARDINAL, MorphologicalTag.CAUSATIVE, MorphologicalTag.DEMONSTRATIVEPRONOUN,
                  MorphologicalTag.DISTRIBUTIVE, MorphologicalTag.FITFOR,
                  MorphologicalTag.FUTUREPARTICIPLE, MorphologicalTag.INFINITIVE, MorphologicalTag.NESS,
                  MorphologicalTag.ORDINAL, MorphologicalTag.PASSIVE,
                  MorphologicalTag.PASTPARTICIPLE, MorphologicalTag.PRESENTPARTICIPLE, MorphologicalTag.QUESTIONPRONOUN,
                  MorphologicalTag.QUANTITATIVEPRONOUN, MorphologicalTag.RANGE,
                  MorphologicalTag.RATIO, MorphologicalTag.REAL, MorphologicalTag.RECIPROCAL,
                  MorphologicalTag.REFLEXIVE, MorphologicalTag.REFLEXIVEPRONOUN,
                  MorphologicalTag.TIME, MorphologicalTag.WHEN, MorphologicalTag.WHILE,
                  MorphologicalTag.WITHOUTHAVINGDONESO, MorphologicalTag.PCABLATIVE,
                  MorphologicalTag.PCACCUSATIVE, MorphologicalTag.PCDATIVE, MorphologicalTag.PCGENITIVE,
                  MorphologicalTag.PCINSTRUMENTAL, MorphologicalTag.PCNOMINATIVE,
                  MorphologicalTag.ACQUIRE, MorphologicalTag.ACTOF, MorphologicalTag.AFTERDOINGSO,
                  MorphologicalTag.ALMOST, MorphologicalTag.AS,
                  MorphologicalTag.ASIF, MorphologicalTag.BECOME, MorphologicalTag.EVERSINCE, MorphologicalTag.FEELLIKE,
                  MorphologicalTag.HASTILY,
                  MorphologicalTag.INBETWEEN, MorphologicalTag.JUSTLIKE, MorphologicalTag.LY,
                  MorphologicalTag.NOTABLESTATE, MorphologicalTag.RELATED,
                  MorphologicalTag.REPEAT, MorphologicalTag.SINCE, MorphologicalTag.SINCEDOINGSO,
                  MorphologicalTag.START, MorphologicalTag.STAY,
                  MorphologicalTag.EQUATIVE, MorphologicalTag.INSTRUMENTAL, MorphologicalTag.AORIST,
                  MorphologicalTag.DESIRE, MorphologicalTag.FUTURE,
                  MorphologicalTag.IMPERATIVE, MorphologicalTag.NARRATIVE, MorphologicalTag.NECESSITY,
                  MorphologicalTag.OPTATIVE, MorphologicalTag.PAST,
                  MorphologicalTag.PRESENT, MorphologicalTag.PROGRESSIVE1, MorphologicalTag.PROGRESSIVE2,
                  MorphologicalTag.CONDITIONAL, MorphologicalTag.COPULA,
                  MorphologicalTag.POSITIVE, MorphologicalTag.PRONOUN, MorphologicalTag.LOCATIVE,
                  MorphologicalTag.RELATIVE, MorphologicalTag.DEMONSTRATIVE,
                  MorphologicalTag.INFINITIVE2, MorphologicalTag.INFINITIVE3, MorphologicalTag.BEGINNINGOFSENTENCE,
                  MorphologicalTag.ENDOFSENTENCE, MorphologicalTag.BEGINNINGOFTITLE,
                  MorphologicalTag.ENDOFTITLE, MorphologicalTag.BEGINNINGOFDOCUMENT, MorphologicalTag.ENDOFDOCUMENT,
                  MorphologicalTag.INFINITIVE, MorphologicalTag.ASLONGAS,
                  MorphologicalTag.DISTRIBUTIVE, MorphologicalTag.ADAMANTLY, MorphologicalTag.PERCENT,
                  MorphologicalTag.WITHOUTBEINGABLETOHAVEDONESO, MorphologicalTag.DIMENSION,
                  MorphologicalTag.PERSONALPRONOUN, MorphologicalTag.FRACTION, MorphologicalTag.HASHTAG,
                  MorphologicalTag.EMAIL, MorphologicalTag.DATE]

    def __init__(self, IG: str):
        """
        A constructor of InflectionalGroup class which initializes the IG list by parsing given input
        String IG by + and calling the getMorphologicalTag method with these substrings. If getMorphologicalTag method
        returns a tag, it adds this tag to the IG list.

        PARAMETERS
        ----------
        IG : str
            String input.
        """
        self.__IG = []
        st = IG
        while "+" in st:
            morphologicalTag = st[:st.index("+")]
            tag = InflectionalGroup.getMorphologicalTag(morphologicalTag)
            if tag is not None:
                self.__IG.append(tag)
            else:
                print("Morphological Tag " + morphologicalTag + " not found")
            st = st[st.index("+") + 1:]
        morphologicalTag = st
        tag = InflectionalGroup.getMorphologicalTag(morphologicalTag)
        if tag is not None:
            self.__IG.append(tag)
        else:
            print("Morphological Tag " + morphologicalTag + " not found")

    @staticmethod
    def getMorphologicalTag(tag: str) -> MorphologicalTag:
        """
        The getMorphologicalTag method takes a String tag as an input and if the input matches with one of the elements
        of tags array, it then gets the morphoTags of this tag and returns it.

        PARAMETERS
        ----------
        tag : str
            String to get morphoTags from.

        RETURNS
        -------
        MorphologicalTag
            morphoTags if found, None otherwise.
        """
        for j in range(len(InflectionalGroup.tags)):
            if tag == InflectionalGroup.tags[j]:
                return InflectionalGroup.morphotags[j]
        return None

    @staticmethod
    def getTagString(tag: MorphologicalTag) -> str:
        """
        The getTag method takes a MorphologicalTag type tag as an input and returns its corresponding tag from tags
        array.

        PARAMETERS
        ----------
        tag : MorphologicalTag
            MorphologicalTag type input to find tag from.

        RETURNS
        -------
        str
            Tag if found, None otherwise.
        """
        for j in range(len(InflectionalGroup.morphotags)):
            if tag == InflectionalGroup.morphotags[j]:
                return InflectionalGroup.tags[j]
        return None

    def getTag(self, index: int) -> MorphologicalTag:
        """
        Another getTag method which takes index as an input and returns the corresponding tag from IG {@link ArrayList}.

        PARAMETERS
        ----------
        index : int
            index to get tag.

        RETURNS
        -------
        MorphologicalTag
            tag at input index.
        """
        return self.__IG[index]

    def size(self) -> int:
        """
        The size method returns the size of the IG list.

        RETURNS
        -------
        int
            the size of the IG list.
        """
        return len(self.__IG)

    def __str__(self) -> str:
        """
        Overridden toString method to return resulting tags in IG list.

        RETURNS
        -------
        str
            String result.
        """
        result = InflectionalGroup.getTagString(self.__IG[0])
        for i in range(1, len(self.__IG)):
            result = result + "+" + InflectionalGroup.getTagString(self.__IG[i])
        return result

    def containsCase(self) -> MorphologicalTag:
        """
        The containsCase method loops through the tags in IG list and finds out the tags of the NOMINATIVE,
        ACCUSATIVE, DATIVE, LOCATIVE or ABLATIVE cases.

        RETURNS
        -------
        MorphologicalTag
            tag which holds the condition.
        """
        for tag in self.__IG:
            if tag == MorphologicalTag.NOMINATIVE or tag == MorphologicalTag.ACCUSATIVE or \
                    tag == MorphologicalTag.DATIVE or tag == MorphologicalTag.LOCATIVE or \
                    tag == MorphologicalTag.ABLATIVE:
                return tag
        return None

    def containsPlural(self) -> bool:
        """
        The containsPlural method loops through the tags in IG list and checks whether the tags are from
        the agreement plural or possessive plural, i.e A1PL, A2PL, A3PL, P1PL, P2PL and P3PL.

        RETURNS
        -------
        bool
            True if the tag is plural, False otherwise.
        """
        for tag in self.__IG:
            if tag == MorphologicalTag.A1PL or tag == MorphologicalTag.A2PL or tag == MorphologicalTag.A3PL or \
                    tag == MorphologicalTag.P1PL or tag == MorphologicalTag.P2PL or tag == MorphologicalTag.P3PL:
                return True
        return False

    def containsTag(self, tag: MorphologicalTag) -> bool:
        """
        The containsTag method takes a MorphologicalTag type tag as an input and loops through the tags in
        IG list and returns true if the input matches with on of the tags in the IG.

        PARAMETERS
        ----------
        tag : MorphologicalTag
            MorphologicalTag type input to search for.

        RETURNS
        -------
        bool
            True if tag matches with the tag in IG, False otherwise.
        """
        for currentTag in self.__IG:
            if tag == currentTag:
                return True
        return False

    def containsPossessive(self) -> bool:
        """
        The containsPossessive method loops through the tags in IG list and returns true if the tag in IG is
        one of the possessives: P1PL, P1SG, P2PL, P2SG, P3PL AND P3SG.

        RETURNS
        -------
        bool
            True if it contains possessive tag, False otherwise.
        """
        for tag in self.__IG:
            if tag == MorphologicalTag.P1SG or tag == MorphologicalTag.P1PL or tag == MorphologicalTag.P2SG or \
                    tag == MorphologicalTag.P2PL or tag == MorphologicalTag.P3SG or tag == MorphologicalTag.P3PL:
                return True
        return False
