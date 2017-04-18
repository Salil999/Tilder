from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import wikipedia
import subprocess
import RAKE.rake as rk


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


def callMIScript(phrase1, phrase2):
	proc = subprocess.Popen(["./js/calcMI.js", "--phrase1=" +
							phrase1, "--phrase2=" + phrase2],
							stdout=subprocess.PIPE)
	line = proc.stdout.readline()
	return line


def calculate_MI(keywords):
	"""
	Calculates the mutual information based on the keywords.

	Args:
	    keywords (TYPE): Description
	
	Returns:
	    TYPE: Description
	"""
	keywordMI = {}
	finalSummary = ""

	keywords = [tup for tup in keywords if tup[1] > 4.0]
	# print(keywords)

	for i in range(5):
		phrase1 = keywords[i][0].encode("ascii", "ignore").decode("ascii")
		if phrase1 != keywords[i][0]:
			continue
		subPhrases = []
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
		subPhrases = [tup[0] for tup in sorted(
			subPhrases, key=lambda tup: tup[1])[::-1][:4]]
		summaryLine = phrase1 + ': ' + ', '.join(subPhrases)
		print(summaryLine)
		finalSummary += summaryLine + '\n'
	print(finalSummary)
	print(keywordMI)
	return finalSummary


def find_keywords(text):
	"""
	This function finds all the keywords.
	
	Args:
		text (string): Where we extract the keywords from
	
	Returns:
		keywords (list): A list of tuples that contains the key words
	"""
	keywords = rk.Rake("SmartStoplist.txt")
	return keywords.run(text)


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
		ret[key] = arr
	else:
		arr = [val]
		ret[key] = arr
	return dictionary


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
