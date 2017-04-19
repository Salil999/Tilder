from collections import Counter
import nltk as nl
from nltk.corpus import stopwords
# import numpy as np
import subprocess

import RAKE.rake as rk

def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)


def import_text(file_path):
    file = open(file_path, 'r')
    data = file.read().replace('\n', ' ')
    return data


def textToFile(text):
    inputFiles = ["input.txt", "../input.txt"]
    for fileName in inputFiles:
        file = open(fileName, "w")
        text = text.replace('\n', '').replace('\r', '')
        file.write(text)
        file.close()


def process_text(text):
    textToFile(text)
    keywords = find_keywords(text)
    return calculate_MI(keywords)

@memoize
def callMIScript(phrase1, phrase2):
    proc = subprocess.Popen(["./js/calcMI.js", "--phrase1="+phrase1, "--phrase2="+phrase2], stdout=subprocess.PIPE)
    line = proc.stdout.readline()
    return line


def calculate_MI(keywords):
    keywordMI = {}
    finalSummary = ""

    keywords = [tup for tup in keywords if tup[1] > 4.0]
    # print(keywords)

    for i in range(5):
        phrase1 = keywords[i][0].encode("ascii", "ignore").decode("ascii")
        if phrase1 != keywords[i][0]:
            continue
        subPhrases=[]
        for j in range(i, len(keywords)):
            phrase2 = keywords[j][0].encode("ascii", "ignore").decode("ascii")
            if phrase2 != keywords[j][0]:
                continue
            if i == j:
                continue
            line = callMIScript(phrase1, phrase2)
            print(phrase1 + " AND " + phrase2)
            print(line)
            mi = float(line)
            subPhrases.append((phrase2, mi))
            # keywordMI[(phrase1, phrase2)] = mi
        # print()
        subPhrases = [tup[0] for tup in sorted(subPhrases, key = lambda tup: tup[1])[::-1][:4]]
        summaryLine = phrase1 + ': ' + ', '.join(subPhrases)
        print(summaryLine)
        finalSummary += summaryLine + '\n'
    print(finalSummary)
    print(keywordMI)
    return finalSummary

def find_keywords(text):
        keywords = rk.Rake("SmartStoplist.txt")
        return keywords.run(text)


#proc = subprocess.Popen(["./js/calcMI.js", "--phrase1=background language model", "--phrase2=pseudocounts"], stdout=subprocess.PIPE)
#print(float(proc.stdout.readline()))


## REFERENCE MATERIAL
    # tokenizer = nl.tokenize.RegexpTokenizer(r'\w+')
    # tokens = tokenizer.tokenize(text)
    # stopWords = set(stopwords.words('english'))
    # words = []
    # for w in tokens:
    #     if w not in stopWords:
    #         words.append(w)

    # bigrams = nl.ngrams(words, 2)
    # trigrams = nl.ngrams(words, 3)

    # print(words)
    # print(Counter(bigrams))
    # print(Counter(trigrams))