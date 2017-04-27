from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import wikipedia
import subprocess
import RAKE.rake as rk
import re


def import_text(file_path):
    file = open(file_path, 'r')
    data = file.read().replace('\n', ' ')
    return data

def wiki_lookup(term):
    raw_content = wikipedia.page(term)
    return process_text(raw_content.content)


def textToFile(text):
    inputFiles = ["input.txt", "../input.txt"]
    for fileName in inputFiles:
        file = open(fileName, "w")
        file.write(text)
        file.close()


def filterKeywords(keywords):
    return keywords #[tup for tup in keywords if (tup[1] > 2.0 and len(tup[0].split(' ')) < 3)]
    


def process_text(text):
    text = text.replace('\n', '').replace('\r', '')
    regex = re.compile("[^\-\w.&\s!\?]")
    regex2 = re.compile("\.(?=\w)")
    regex3 = re.compile("-")
    text = re.sub(regex, '', text)
    text = re.sub(regex2, '. ', text)
    text = re.sub(regex3, ' ', text)
    textToFile(text)
    keywords = find_keywords(text)
    keywords = filterKeywords(keywords)
    print(keywords)
    summary, uniques, deps = calculate_MI(keywords)
    sentenceDict = map_keyphrase_sentence(uniques, text)
    return {"summary": summary, "sentences": sentenceDict, "graph": deps}


def callMIScript(phrase1, phrase2):
    proc = subprocess.Popen(["./js/calcMI.js",
                             "--phrase1=" + phrase1,
                             "--phrase2=" + phrase2],
                            stdout=subprocess.PIPE)
    line = proc.stdout.readline()
    return line


def calculate_MI(keywords):
    dependencies = {}
    finalSummary = ""
    uniqueKeyphrases = set()

    keywords = [tup for tup in keywords if tup[1] > 4.0]
    # print(keywords)

    for i in range(min(5, len(keywords))):
        phrase1 = keywords[i][0].encode("ascii", "ignore").decode("ascii")
        if phrase1 != keywords[i][0]:
            continue
        subPhrases = []
        dependencies[phrase1] = []
        if phrase1 not in uniqueKeyphrases:
            uniqueKeyphrases.add(phrase1)
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
        # print()
        subPhrases = [tup[0] for tup in sorted(
            subPhrases, key=lambda tup: tup[1])[::-1][:4]]
        summaryLine = phrase1 + ': ' + ', '.join(subPhrases)
        for elem in subPhrases:
            arr = dependencies[phrase1]
            arr.append(elem)
            dependencies[phrase1] = arr
            if elem not in uniqueKeyphrases:
                uniqueKeyphrases.add(elem)
        print(summaryLine)
        finalSummary += summaryLine + '\n'
    print(list(uniqueKeyphrases))
    print(finalSummary)
    return finalSummary, uniqueKeyphrases, dependencies


def find_keywords(text):
    """
    This function finds all the keywords.

    Args:
            text (string): Where we extract the keywords from

    Returns:
            keywords (list): A list of tuples that contains the key words
    """
    keywords = rk.Rake("SmartStoplist.txt", 4, 4, 2)
    words = keywords.run(text)
    return words


def map_keyphrase_sentence(key_phrase, text):
    """
    This function maps the key phrases into each sentence the
    key phrases are present in.

    Args:
            key_phrase (list): List of key phrases
            text (string): Big body of input text

    Returns:
            ret (dict): A mapping of the key phrases to each sentence it is in
    """

    ret = dict()
    # we split the blob of text into sentences
    split_text = sent_tokenize(text)
    for sentence in split_text:
        for phrase in key_phrase:
            # checks to see if a phrase is in a sentence
            if(phrase in sentence):
                ret = add_to_dict(ret, phrase, sentence)
    return ret


def add_to_dict(dictionary, key, val):
    """
    This function adds an item to a dictionary. Just some helper code.

    Args:
            dictionary (dict): The dictionary we want to add an item to
            key (string): The key of the dictionary
            val (val): The value we want to add into the dictionary

    Returns:
            dictionary (dict): The dictionary with the added value
    """
    if(key in dictionary):
        arr = dictionary.get(key)
        arr.append(val)
        dictionary[key] = arr
    else:
        arr = [val]
        dictionary[key] = arr
    return dictionary


# calculate_MI(find_keywords(import_text("input.txt")))
#proc = subprocess.Popen(["./js/calcMI.js", "--phrase1=background language model", "--phrase2=pseudocounts"], stdout=subprocess.PIPE)
# print(float(proc.stdout.readline()))


# REFERENCE MATERIAL
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
