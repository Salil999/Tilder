import nltk as nl
from nltk.corpus import stopwords

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

    print(words)
    return 0


process_text(import_text('input.txt'))