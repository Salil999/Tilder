import nltk as nl


def import_text(file_path):
    file = open(file_path, 'r')
    data = file.read().replace('\n', ' ')
    return data


def process_text(text):
    
    return 0


process_text(import_text('input.txt'))