import textrank as tr


def summarize_string_data(text):
    summary = tr.extract_sentences(text)
    return summary


def import_text(file_path):
    file = open(file_path, 'r')
    data = file.read().replace('\n', ' ')
    return data


print(summarize_string_data(import_text('input.txt')))
