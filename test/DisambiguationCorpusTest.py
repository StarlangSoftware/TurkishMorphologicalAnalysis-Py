import unittest
from DisambiguationCorpus.DisambiguationCorpus import DisambiguationCorpus


class MyTestCase(unittest.TestCase):

    def test_Corpus(self):
        corpus = DisambiguationCorpus("../penntreebank.txt")
        self.assertEqual(19109, corpus.sentenceCount())
        self.assertEqual(170211, corpus.numberOfWords())


if __name__ == '__main__':
    unittest.main()
