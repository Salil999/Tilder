import nltk as nl
from nltk.corpus import stopwords
from collections import Counter

import RAKE.rake as rk

def import_text(file_path):
    file = open(file_path, 'r')
    data = file.read().replace('\n', ' ')
    return data


def process_text(text):
    tokenizer = nl.tokenize.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    stopWords = set(stopwords.words('english'))
    words = []
    for w in tokens:
        if w not in stopWords:
            words.append(w)

    bigrams = nl.ngrams(words, 2)
    trigrams = nl.ngrams(words, 3)

    print(words)
    print(Counter(bigrams))
    print(Counter(trigrams))
    return "SUMMARY"


def find_keywords(text):
        keywords = rk.Rake("SmartStoplist.txt")
        return keywords.run(text)


print(find_keywords(import_text("input.txt")))
