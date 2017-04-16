import nltk as nl
from nltk.corpus import stopwords
from collections import Counter
import subprocess

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

def calculate_MI(keywords):
    keywordMI = {}

    print(keywords)

    for i in range(len(keywords)):
        phrase1 = keywords[i][0].encode("ascii", "ignore").decode("ascii")
        if phrase1 != keywords[i][0]:
                continue
        for j in range(len(keywords)):
            phrase2 = keywords[j][0].encode("ascii", "ignore").decode("ascii")
            if phrase2 != keywords[j][0]:
                continue
            proc = subprocess.Popen(["./js/calcMI.js", "--phrase1="+phrase1, "--phrase2="+phrase2], stdout=subprocess.PIPE)
            line = proc.stdout.readline()
            print(phrase1 + " AND " + phrase2)
            print(line)
            mi = float(line)
            keywordMI[(phrase1, phrase2)] = mi

    print(keywordMI)
    return 0

def find_keywords(text):
        keywords = rk.Rake("SmartStoplist.txt")
        return keywords.run(text)


keywords = find_keywords(import_text("input.txt"))
calculate_MI(keywords)

#proc = subprocess.Popen(["./js/calcMI.js", "--phrase1=background language model", "--phrase2=pseudocounts"], stdout=subprocess.PIPE)
#print(float(proc.stdout.readline()))
