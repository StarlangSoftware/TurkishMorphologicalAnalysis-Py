from Corpus.Corpus import Corpus
from Corpus.Sentence import Sentence

from DisambiguationCorpus.DisambiguatedWord import DisambiguatedWord
from MorphologicalAnalysis.MorphologicalParse import MorphologicalParse


class DisambiguationCorpus(Corpus):

    def __init__(self, fileName=None):
        """
        Constructor which creates a list of sentences and a CounterHashMap of wordList.
        """
        super().__init__()
        if fileName is not None:
            input_file = open(fileName, "r", encoding="utf8")
            lines = input_file.readlines()
            new_sentence = Sentence()
            for line in lines:
                word = line[:line.index("\t")]
                parse = line[line.index("\t") + 1:]
                if len(word) > 0 and len(parse) > 0:
                    new_word = DisambiguatedWord(word, MorphologicalParse(parse.strip()))
                    if word == "<S>":
                        new_sentence = Sentence()
                    elif word == "</S>":
                        self.addSentence(new_sentence)
                    elif word == "<DOC>" or word == "</DOC>" or word == "<TITLE>" or word == "</TITLE>":
                        pass
                    else:
                        new_sentence.addWord(new_word)
            input_file.close()

    def writeToFile(self, fileName: str):
        """
        The writeToFile method takes a str file name as an input and writes the elements of sentences list
        to this file with proper tags which indicates the beginnings and endings of the document and sentence.

        PARAMETERS
        ----------
        fileName : str
            File which will be filled with the sentences.
        """
        output_file = open(fileName, "w", encoding="utf8")
        output_file.write("<DOC>\t<DOC>+BDTag\n")
        for sentence in self.sentences:
            output_file.write("<S>\t<S>+BSTag\n")
            for word in sentence.words:
                if isinstance(word, DisambiguatedWord):
                    output_file.write(word.getName() + "\t" + word.getParse().__str__() + "\n")
            output_file.write("</S>\t</S>+ESTag\n")
        output_file.write("</DOC>\t</DOC>+EDTag")
        output_file.close()
