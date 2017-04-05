import metapy as mp


def import_text(file_path):
    file = open(file_path, 'r')
    data = file.read().replace('\n', ' ')
    return data


def process_text(text):
    doc = mp.index.Document()
    doc.content(text)

    # Tokenization and stop word elimination
    tok = mp.analyzers.ICUTokenizer(suppress_tags = True)
    tok.set_content(doc.content())
    tok = mp.analyzers.LengthFilter(tok, min=2, max=30)  # Remove very short or long words
    tok = mp.analyzers.ListFilter(tok, 'lemur-stopwords.txt', mp.analyzers.ListFilter.Type.Reject)

    ana = mp.analyzers.NGramWordAnalyzer(2, tok)

    ana = ana.analyze(doc)

    for a in ana:
        if (ana[a] > 8):
            print(a)

    ana3 = mp.analyzers.NGramWordAnalyzer(3, tok)

    ana3 = ana3.analyze(doc)

    for a in ana3:
        if (ana3[a] > 6):
            print(a)

    # print(ana)

    # print([token for token in tok])


process_text(import_text('input.txt'))

