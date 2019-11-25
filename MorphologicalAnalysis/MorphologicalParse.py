from Dictionary.Word import Word

from MorphologicalAnalysis.InflectionalGroup import InflectionalGroup
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag


class MorphologicalParse:

    inflectionalGroups: list
    root: Word

    """
    Constructor of MorphologicalParse class which takes a String parse as an input. First it creates
    a list as iGs for inflectional groups, and while given String contains derivational boundary (^DB+), it
    adds the substring to the iGs list and continue to use given String from 4th index. If it does not contain ^DB+,
    it directly adds the given String to the iGs list. Then, it creates a new list as
    inflectionalGroups and checks for some cases.
    
    If the first item of iGs list is ++Punc, it creates a new root as +, and by calling
    InflectionalGroup method with Punc it initializes the IG list by parsing given input
    String IG by + and calling the getMorphologicalTag method with these substrings. If getMorphologicalTag method 
    returns a tag, it adds this tag to the IG list and also to the inflectionalGroups list.

    If the first item of iGs list has +, it creates a new word of first item's substring from index 0 to +,
    and assigns it to root. Then, by calling InflectionalGroup method with substring from index 0 to +,
    it initializes the IG list by parsing given input String IG by + and calling the getMorphologicalTag
    method with these substrings. If getMorphologicalTag method returns a tag, it adds this tag to the IG list
    and also to the inflectionalGroups list.

    If the first item of iGs list does not contain +, it creates a new word with first item and assigns it as root.
    At the end, it loops through the items of iGs and by calling InflectionalGroup method with these items
    it initializes the IG list by parsing given input String IG by + and calling the getMorphologicalTag
    method with these substrings. If getMorphologicalTag method returns a tag, it adds this tag to the IG list
    and also to the inflectionalGroups list.

    PARAMETERS
    ----------
    parse : str
        String input.
    """
    def __init__(self, parse:None):
        if parse is not None:
            if isinstance(parse, str):
                iGs = []
                st = parse
                while "^DB+" in st:
                    iGs.append(st[:st.index("^DB+")])
                    st = st[st.index("^DB+") + 4:]
                iGs.append(st)
                self.inflectionalGroups = []
                if iGs[0] == "++Punc":
                    self.root = Word("+")
                    self.inflectionalGroups.append(InflectionalGroup("Punc"))
                else:
                    if iGs[0].index("+") != -1:
                        self.root = Word(iGs[0][:iGs[0].index("+")])
                        self.inflectionalGroups.append(InflectionalGroup(iGs[0][iGs[0].index("+") + 1:]))
                    else:
                        self.root = Word(iGs[0])
                    for i in range(1, len(iGs)):
                        self.inflectionalGroups.append(InflectionalGroup(iGs[i]))
            elif isinstance(parse, list):
                self.inflectionalGroups = []
                if parse[0].index("+") != -1:
                    self.root = Word(parse[0][:parse[0].index("+")])
                    self.inflectionalGroups.append(InflectionalGroup(parse[0][parse[0].index("+") + 1:]))
                for i in range(1, len(parse)):
                    self.inflectionalGroups.append(InflectionalGroup(parse[i]))

    """
    The no-arg getWord method returns root Word.

    RETURNS
    -------
    Word
        root Word.
    """
    def getWord(self) -> Word:
        return self.root

    """
    The getTransitionList method gets the first item of inflectionalGroups list as a str, then loops
    through the items of inflectionalGroups and concatenates them by using +.

    RETURNS
    -------
    str
        String that contains transition list.
    """
    def getTransitionList(self) -> str:
        result = self.inflectionalGroups[0].__str__()
        for i in range(1, len(self.inflectionalGroups)):
            result = result + "+" + self.inflectionalGroups[i].__str__()
        return result

    """
    The getInflectionalGroupString method takes an int index as an input and if index is 0, it directly returns the
    root and the first item of inflectionalGroups list. If the index is not 0, it then returns the corresponding
    item of inflectionalGroups list as a str.

    PARAMETERS
    ----------
    index : int
        Integer input.
        
    RETURNS
    -------
    str
        Corresponding item of inflectionalGroups at given index as a str.
    """
    def getInflectionalGroupString(self, index: int) -> str:
        if index == 0:
            return self.root.getName() + "+" + self.inflectionalGroups[0].__str__()
        else:
            return self.inflectionalGroups[index].__str__()

    """
    The getInflectionalGroup method takes an integer index as an input and it directly returns the {InflectionalGroup
    at given index.

    PARAMETERS
    ----------
    index : int
        Integer input.
        
    RETURNS
    -------
    InflectionalGroup
        InflectionalGroup at given index.
    """
    def getInflectionalGroup(self, index: int) -> InflectionalGroup:
        return self.inflectionalGroups[index]

    """
    The getLastInflectionalGroup method directly returns the last InflectionalGroup of inflectionalGroups list.

    RETURNS
    -------
    InflectionalGroup
        The last InflectionalGroup of inflectionalGroups list.
    """
    def getLastInflectionalGroup(self) -> InflectionalGroup:
        return self.inflectionalGroups[len(self.inflectionalGroups) - 1]

    """
    The getTag method takes an integer index as an input and and if the given index is 0, it directly return the root.
    then, it loops through the inflectionalGroups list it returns the MorphologicalTag of the corresponding inflectional 
    group.

    PARAMETERS
    ----------
    index : int
        Integer input.
        
    RETURNS
    -------
    str
        The MorphologicalTag of the corresponding inflectional group, or null of invalid index inputs.
    """
    def getTag(self, index: int) -> str:
        size = 1
        if index == 0:
            return self.root.getName()
        for group in self.inflectionalGroups:
            if index < size + group.size():
                return InflectionalGroup.getTagString(group.getTag(index - size))
            size += group.size()
        return None

    """
    The tagSize method loops through the inflectionalGroups list and accumulates the sizes of each inflectional group
    in the inflectionalGroups.

    RETURNS
    -------
    int
        Total size of the inflectionalGroups list.
    """
    def tagSize(self) -> int:
        size = 1
        for group in self.inflectionalGroups:
            size += group.size()
        return size

    """
    The size method returns the size of the inflectionalGroups list.

    RETURNS
    -------
    int
        The size of the inflectionalGroups list.
    """
    def size(self) -> int:
        return len(self.inflectionalGroups)

    """
    The firstInflectionalGroup method returns the first inflectional group of inflectionalGroups list.

    RETURNS
    -------
    InflectionalGroup
        The first inflectional group of inflectionalGroups list.
    """
    def firstInflectionalGroup(self) -> InflectionalGroup:
        return self.inflectionalGroups[0]

    """
    The lastInflectionalGroup method returns the last inflectional group of inflectionalGroups list.

    RETURNS
    -------
    InflectionalGroup
        The last inflectional group of inflectionalGroups list.
    """
    def lastInflectionalGroup(self) -> InflectionalGroup:
        return self.inflectionalGroups[len(self.inflectionalGroups) - 1]

    """
    The getWordWithPos method returns root with the MorphologicalTag of the first inflectional as a new word.

    RETURNS
    -------
    Word
        Root with the MorphologicalTag of the first inflectional as a new word.
    """
    def getWordWithPos(self) -> Word:
        return Word(self.root.getName() + "+" + InflectionalGroup.getTagString(self.firstInflectionalGroup().getTag(0)))

    """
    The getPos method returns the MorphologicalTag of the last inflectional group.

    RETURNS
    -------
    str
        The MorphologicalTag of the last inflectional group.
    """
    def getPos(self) -> str:
        return InflectionalGroup.getTagString(self.lastInflectionalGroup().getTag(0))

    """
    The getRootPos method returns the MorphologicalTag of the first inflectional group.

    RETURNS
    -------
    str
        The MorphologicalTag of the first inflectional group.
    """
    def getRootPos(self) -> str:
        return InflectionalGroup.getTagString(self.firstInflectionalGroup().getTag(0))

    """
    The lastIGContainsCase method returns the MorphologicalTag of last inflectional group if it is one of the 
    NOMINATIVE, ACCUSATIVE, DATIVE, LOCATIVE or ABLATIVE cases, null otherwise.

    RETURNS
    -------
    str
        The MorphologicalTag of last inflectional group if it is one of the NOMINATIVE, ACCUSATIVE, DATIVE, LOCATIVE or 
        ABLATIVE cases, null otherwise.
    """
    def lastIGContainsCase(self) -> str:
        caseTag = self.lastInflectionalGroup().containsCase()
        if caseTag is not None:
            return InflectionalGroup.getTagString(caseTag)
        else:
            return "NULL"

    """
    The lastIGContainsTag method takes a MorphologicalTag as an input and returns true if the last inflectional group's
    MorphologicalTag matches with one of the tags in the IG list, false otherwise.

    PARAMETERS
    ----------
    tag : MorphologicalTag
        MorphologicalTag type input.
        
    RETURNS
    -------
    bool
        True if the last inflectional group's MorphologicalTag matches with one of the tags in the IG list, False 
        otherwise.
    """
    def lastIGContainsTag(self, tag: MorphologicalTag) -> bool:
        return self.lastInflectionalGroup().containsTag(tag)

    """
    lastIGContainsPossessive method returns true if the last inflectional group contains one of the
    possessives: P1PL, P1SG, P2PL, P2SG, P3PL AND P3SG, false otherwise.

    RETURNS
    -------
    bool
        True if the last inflectional group contains one of the possessives: P1PL, P1SG, P2PL, P2SG, P3PL AND P3SG, 
        false otherwise.
    """
    def lastIGContainsPossessive(self) -> bool:
        return self.lastInflectionalGroup().containsPossessive()

    """
    The isCapitalWord method returns True if the character at first index of root is an uppercase letter, False 
    otherwise.

    RETURNS
    -------
    bool
        True if the character at first index of root is an uppercase letter, False otherwise.
    """
    def isCapitalWord(self) -> bool:
        return self.root.getName()[0:0].isupper()

    """
    The isNoun method returns true if the past of speech is NOUN, False otherwise.

    RETURNS
    -------
    bool
        True if the past of speech is NOUN, False otherwise.
    """
    def isNoun(self) -> bool:
        return self.getPos() == "NOUN"

    """
    The isVerb method returns true if the past of speech is VERB, False otherwise.

    RETURNS
    -------
    bool
        True if the past of speech is VERB, False otherwise.
    """
    def isVerb(self) -> bool:
        return self.getPos() == "VERB"

    """
    The isRootVerb method returns True if the past of speech of root is BERV, False otherwise.

    RETURNS
    -------
    bool
        True if the past of speech of root is VERB, False otherwise.
    """
    def isRootVerb(self) -> bool:
        return self.getRootPos() == "VERB"

    """
    The isAdjective method returns True if the past of speech is ADJ, False otherwise.

    RETURNS
    -------
    bool
        True if the past of speech is ADJ, False otherwise.
    """
    def isAdjective(self) -> bool:
        return self.getPos() == "ADJ"

    """
    The isProperNoun method returns True if the first inflectional group's MorphologicalTag is a PROPERNOUN, False 
    otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a PROPERNOUN, False otherwise.
    """
    def isProperNoun(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.PROPERNOUN)

    """
    The isPunctuation method returns True if the first inflectional group's MorphologicalTag is a PUNCTUATION, False 
    otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a PUNCTUATION, False otherwise.
    """
    def isPunctuation(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.PUNCTUATION)

    """
    The isCardinal method returns True if the first inflectional group's MorphologicalTag is a CARDINAL, False 
    otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a CARDINAL, False otherwise.
    """
    def isCardinal(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.CARDINAL)

    """
    The isOrdinal method returns True if the first inflectional group's MorphologicalTag is a ORDINAL, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a ORDINAL, False otherwise.
    """
    def isOrdinal(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.ORDINAL)

    """
    The isReal method returns True if the first inflectional group's MorphologicalTag is a REAL, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a REAL, False otherwise.
    """
    def isReal(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.REAL)

    """
    The isNumber method returns True if the first inflectional group's MorphologicalTag is REAL or CARDINAL, False 
    otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a REAL or CARDINAL, False otherwise.
    """
    def isNumber(self) -> bool:
        return self.isReal() or self.isCardinal()

    """
    The isTime method returns True if the first inflectional group's MorphologicalTag is a TIME, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a TIME, False otherwise.
    """
    def isTime(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.TIME)

    """
    The isDate method returns True if the first inflectional group's MorphologicalTag is a DATE, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a DATE, False otherwise.
    """
    def isDate(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.DATE)

    """
    The isHashTag method returns True if the first inflectional group's MorphologicalTag is a HASHTAG, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a HASHTAG, False otherwise.
    """
    def isHashTag(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.HASHTAG)

    """
    The isEmail method returns True if the first inflectional group's MorphologicalTag is a EMAIL, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a EMAIL, False otherwise.
    """
    def isEmail(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.EMAIL)

    """
    The isPercent method returns True if the first inflectional group's MorphologicalTag is a PERCENT, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a PERCENT, False otherwise.
    """
    def isPercent(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.PERCENT)

    """
     The isFraction method returns True if the first inflectional group's MorphologicalTag is a FRACTION, False 
     otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a FRACTION, False otherwise.
    """
    def isFraction(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.FRACTION)

    """
    The isRange method returns True if the first inflectional group's MorphologicalTag is a RANGE, False otherwise.

    RETURNS
    -------
    bool
        True if the first inflectional group's MorphologicalTag is a RANGE, False otherwise.
    """
    def isRange(self) -> bool:
        return self.getInflectionalGroup(0).containsTag(MorphologicalTag.RANGE)

    """
    The isPlural method returns true if InflectionalGroup's MorphologicalTags are from the agreement plural
    or possessive plural, i.e A1PL, A2PL, A3PL, P1PL, P2PL or P3PL, and False otherwise.

    RETURNS
    -------
    bool
        True if InflectionalGroup's MorphologicalTags are from the agreement plural or possessive plural.
    """
    def isPlural(self) -> bool:
        for inflectionalGroup in self.inflectionalGroups:
            if inflectionalGroup.containsPlural():
                return True
        return False

    """
    The isAuxiliary method returns true if the root equals to the et, ol, or yap, and false otherwise.

    RETURNS
    -------
    bool
        True if the root equals to the et, ol, or yap, and False otherwise.
    """
    def isAuxiliary(self) -> bool:
        return self.root.getName() == "et" or self.root.getName() == "ol" or self.root.getName() == "yap"

    """
    The containsTag method takes a MorphologicalTag as an input and loops through the inflectionalGroups list,
    returns True if the input matches with on of the tags in the IG, False otherwise.

    PARAMETERS
    ----------
    tag : MorphologicalTag
        checked tag
        
    RETURNS
    -------
    bool
        True if the input matches with on of the tags in the IG, False otherwise.
    """
    def containsTag(self, tag: MorphologicalTag) -> bool:
        for inflectionalGroup in self.inflectionalGroups:
            if inflectionalGroup.containsTag(tag):
                return True
        return False

    """
    The getTreePos method returns the tree pos tag of a morphological analysis.

    RETURNS
    -------
    bool
        Tree pos tag of the morphological analysis in string form.
    """
    def getTreePos(self) -> str:
        if self.isProperNoun():
            return "NP"
        elif self.isVerb():
            return "VP"
        elif self.isAdjective():
            return "ADJP"
        elif self.isNoun():
            return "NP"
        elif self.containsTag(MorphologicalTag.ADVERB):
            return "ADVP"
        elif self.isCardinal():
            return "QP"
        elif self.containsTag(MorphologicalTag.POSTPOSITION):
            return "PP"
        elif self.containsTag(MorphologicalTag.CONJUNCTION):
            return "CONJP"
        elif self.containsTag(MorphologicalTag.DETERMINER):
            return "DP"
        elif self.containsTag(MorphologicalTag.INTERJECTION):
            return "INTJ"
        elif self.containsTag(MorphologicalTag.QUESTIONPRONOUN):
            return "WP"
        elif self.containsTag(MorphologicalTag.PRONOUN):
            return "NP"
        else:
            return "-XXX-"

    """
    The overridden toString method gets the root and the first inflectional group as a result String then concatenates
    with ^DB+ and the following inflectional groups.

    RETURNS
    -------
    str
        result str.
    """
    def __str__(self):
        result = self.root.getName() + "+" + self.inflectionalGroups[0].__str__()
        for i in range(1, len(self.inflectionalGroups)):
            result = result + "^^B+" + self.inflectionalGroups[i].__str__()
        return result
