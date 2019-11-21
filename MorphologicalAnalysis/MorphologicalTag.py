from __future__ import annotations
from enum import Enum, auto


class MorphologicalTag(Enum):

    """
    Noun : Alengir
    """
    NOUN = auto()
    """
    Adverb : Alelacele
    """
    ADVERB = auto()
    """
    Adjective : Alengirli
    """
    ADJECTIVE = auto()
    """
    Verb : Alıkoy
    """
    VERB = auto()
    """
    1st person singular agreement : Ben gelirim
    """
    A1SG = auto()
    """
    2nd person singular agreement : Sen gelirsin
    """
    A2SG = auto()
    """
    3rd person singular agreement : O gelir
    """
    A3SG = auto()
    """
    1st person plural agreement : Biz geliriz
    """
    A1PL = auto()
    """
    2nd person plural agreement : Siz gelirsiniz
    """
    A2PL = auto()
    """
    3rd person plural agreement : Onlar gelirler
    """
    A3PL = auto()
    """
    1st person singular possessive : Benim
    """
    P1SG = auto()
    """
    2nd person singular possessive :Senin
    """
    P2SG = auto()
    """
    3rd person singular possessive : Onun
    """
    P3SG = auto()
    """
    1st person plural possessive :  Bizim
    """
    P1PL = auto()
    """
    2nd person plural possessive : Sizin
    """
    P2PL = auto()
    """
    3rd person plural possessive : Onların
    """
    P3PL = auto()
    """
    Proper noun : John
    """
    PROPERNOUN = auto()
    """
    None possessive : Ev
    """
    PNON = auto()
    """
    Nominative Case : Kedi uyuyor.
    """
    NOMINATIVE = auto()
    """
    With : Kalemle
    """
    WITH = auto()
    """
    Without : Dikişsiz
    """
    WITHOUT = auto()
    """
    Accusatıve : Beni
    """
    ACCUSATIVE = auto()
    """
    Dative case : Bana
    """
    DATIVE = auto()
    """
    Genitive : Benim
    """
    GENITIVE = auto()
    """
    Ablative : Okuldan
    """
    ABLATIVE = auto()
    """
    Perosnal pronoun : O
    """
    PERSONALPRONOUN = auto()
    """
    Zero Derivation : Kırmızıydı
    """
    ZERO = auto()
    """
    Ability = auto() possibility : Olabilir
    """
    ABLE = auto()
    """
    Negative : Yapama
    """
    NEGATIVE = auto()
    """
    Past tense : Gitti
    """
    PASTTENSE = auto()
    """
    Conjunction or disjunction : Ama = auto() ise
    """
    CONJUNCTION = auto()
    """
    Determiner : Birtakım
    """
    DETERMINER = auto()
    """
    Duplication : Çıtır çıtır
    """
    DUPLICATION = auto()
    """
    Interjection : Agucuk
    """
    INTERJECTION = auto()
    """
    Number : bir
    """
    NUMBER = auto()
    """
    Post posıtıon : Atfen
    """
    POSTPOSITION = auto()
    """
    Punctuation : +
    """
    PUNCTUATION = auto()
    """
    Question : Mı
    """
    QUESTION = auto()
    """
    Agent : Toplayıcı
    """
    AGENT = auto()
    """
    By doing so : Zıplayarak
    """
    BYDOINGSO = auto()
    """
    Cardinal : yüz = auto() bin
    """
    CARDINAL = auto()
    """
    Causative Form : Pişirmek
    """
    CAUSATIVE = auto()
    """
    Demonstrative pronoun : Bu = auto() şu
    """
    DEMONSTRATIVEPRONOUN = auto()
    """
    Distributive : altışar
    """
    DISTRIBUTIVE = auto()
    """
    Fit for : Ahmetlik
    """
    FITFOR = auto()
    """
    Future participle : Gülecek
    """
    FUTUREPARTICIPLE = auto()
    """
    Infinitive : Biri
    """
    INFINITIVE = auto()
    """
    Ness : Ağırbaşlılık
    """
    NESS = auto()
    """
    Ordinal Number : Altıncı
    """
    ORDINAL = auto()
    """
    Passive : Açıldı
    """
    PASSIVE = auto()
    """
    Past participle : Kırılmış
    """
    PASTPARTICIPLE = auto()
    """
    Present partıcıple : Sarılan
    """
    PRESENTPARTICIPLE = auto()
    """
    Question pronoun : Kim
    """
    QUESTIONPRONOUN = auto()
    """
    Quantitative pronoun : Each
    """
    QUANTITATIVEPRONOUN = auto()
    """
    Range : 1 - 3
    """
    RANGE = auto()
    """
    Ratio : 1/2
    """
    RATIO = auto()
    """
    Real : 1.0
    """
    REAL = auto()
    """
    Reciprocal verb : Görüşmek
    """
    RECIPROCAL = auto()
    """
    Reflexive : Kendi
    """
    REFLEXIVE = auto()
    """
    Reflexive pronoun : Kendim
    """
    REFLEXIVEPRONOUN = auto()
    """
    Time : 14:28
    """
    TIME = auto()
    """
    When : Okuyunca
    """
    WHEN = auto()
    """
    While : Gelirken
    """
    WHILE = auto()
    """
    Without having done so : Çaktırmadan
    """
    WITHOUTHAVINGDONESO = auto()
    """
    PC ablative : Başka
    """
    PCABLATIVE = auto()
    """*
    PC accusative : Takiben
    """
    PCACCUSATIVE = auto()
    """
    PC dative : İlişkin
    """
    PCDATIVE = auto()
    """
    PC genitive : Yanısıra
    """
    PCGENITIVE = auto()
    """
    PC instrumental : Birlikte
    """
    PCINSTRUMENTAL = auto()
    """
    PC nominative
    """
    PCNOMINATIVE = auto()
    """
    Acquire : Kazanılan
    """
    ACQUIRE = auto()
    """
    Act of : Aldatmaca
    """
    ACTOF = auto()
    """
    After doing so : Yapıp
    """
    AFTERDOINGSO = auto()
    """
    Almost : Dikensi
    """
    ALMOST = auto()
    """
    As : gibi
    """
    AS = auto()
    """
    As if : Yaşarmışcasına
    """
    ASIF = auto()
    """
    Become : Abideleş
    """
    BECOME = auto()
    """
    Ever since : Çıkagel
    """
    EVERSINCE = auto()
    """
    Projection : Öpülesi
    """
    FEELLIKE = auto()
    """
    Hastility : Yapıver
    """
    HASTILY = auto()
    """
    In between : Arasında
    """
    INBETWEEN = auto()
    """
    Just like : Destansı
    """
    JUSTLIKE = auto()
    """
    -LY : Akıllıca
    """
    LY = auto()
    """
    Related to : Davranışsal
    """
    RELATED = auto()
    """
    Continuous : Yapadur
    """
    REPEAT = auto()
    """
    Since doing so : Amasyalı
    """
    SINCE = auto()
    """
    Since doing so : Amasyalı
    """
    SINCEDOINGSO = auto()
    """
    Start : Alıkoy
    """
    START = auto()
    """
    Stay : Bakakal
    """
    STAY = auto()
    """
    Equative : Öylece
    """
    EQUATIVE = auto()
    """
    Instrumental : Kışın = auto() arabayla
    """
    INSTRUMENTAL = auto()
    """
    Aorist Tense : Her hafta sonunda futbol oynarlar.
    """
    AORIST = auto()
    """
    Desire/Past Auxiliary : Çıkarsa
    """
    DESIRE = auto()
    """
    Future : Yağacak
    """
    FUTURE = auto()
    """
    Imperative : Otur!
    """
    IMPERATIVE = auto()
    """
    Narrative Past Tense : Oluşmuş
    """
    NARRATIVE = auto()
    """
    Necessity : Yapmalı
    """
    NECESSITY = auto()
    """
    Optative : Doğanaya
    """
    OPTATIVE = auto()
    """
    Past tense : Gitti
    """
    PAST = auto()
    """
    Present partıcıple : Sarılan
    """
    PRESENT = auto()
    """
    Progressive : Görüyorum
    """
    PROGRESSIVE1 = auto()
    """
    Progressive : Görmekteyim
    """
    PROGRESSIVE2 = auto()
    """
    Conditional : Gelirse
    """
    CONDITIONAL = auto()
    """
    Copula : Mavidir
    """
    COPULA = auto()
    """
    Positive : Gittim
    """
    POSITIVE = auto()
    """
    Pronoun : Ben
    """
    PRONOUN = auto()
    """
    Locative : Aşağıda
    """
    LOCATIVE = auto()
    """
    Relative : Gelenin
    """
    RELATIVE = auto()
    """
    Demonstrative : Bu
    """
    DEMONSTRATIVE = auto()
    """
    Infinitive2 : Gitme
    """
    INFINITIVE2 = auto()
    """
    Infinitive3 : Gidiş
    """
    INFINITIVE3 = auto()
    """
    Sentence beginning header
    """
    BEGINNINGOFSENTENCE = auto()
    """
    Sentence ending header
    """
    ENDOFSENTENCE = auto()
    """
    Title beginning header
    """
    BEGINNINGOFTITLE = auto()
    """
    Title ending header
    """
    ENDOFTITLE = auto()
    """
    Document beginning header
    """
    BEGINNINGOFDOCUMENT = auto()
    """
    Document ending header
    """
    ENDOFDOCUMENT = auto()
    """
    As long as : Yaşadıkça
    """
    ASLONGAS = auto()
    """
    Adamantly
    """
    ADAMANTLY = auto()
    """
    Percent : 15%
    """
    PERCENT = auto()
    """
    Without being able to have done so: kararlamadan
    """
    WITHOUTBEINGABLETOHAVEDONESO = auto()
    """
    Dimension : Küçücük
    """
    DIMENSION = auto()
    """
    Notable state : Anlaşılmazlık
    """
    NOTABLESTATE = auto()
    """
    Fraction : 1/2
    """
    FRACTION = auto()
    """
    Hash tag : #
    """
    HASHTAG = auto()
    """
    E-mail : @
    """
    EMAIL = auto()
    """
    Date : 11/06/2018
    """
    DATE = auto()
