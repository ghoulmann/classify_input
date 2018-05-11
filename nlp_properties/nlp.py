# -*- coding: utf-8 -*-

import nltk

class NLP():

    def __init__(self, text):
        self.sentences = nltk.sent_tokenize(text)
        for sentence in self.sentences:
            self.words = nltk.word_tokenize(sentence)
            self.tagged_words = nltk.pos_tag(self.words)
            self.ne_tagged_words = nltk.ne_chunk(self.tagged_words)
            print self.ne_tagged_words
