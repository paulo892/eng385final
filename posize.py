import argparse
import os
import spacy
import ast
import copy 
import math
from collections import Counter
import matplotlib.pyplot as plt

def roundy(dic):
	# truncates each of the proportions to hundredths place
	trunc = copy.deepcopy(dic)
	for key in trunc:
		trunc[key] = math.trunc(trunc[key] * 100) / 100

	# sums the values and subtracts from 1
	diff = (1 - sum(trunc.values()))

	# rounds the difference off
	diff = math.trunc(round(diff * 100)) / 100

	rem = int(diff * 100)
	for key in trunc:
		trunc[key] = trunc[key] * 100

	# while int > 0...
	while (rem > 0):
		# for each key, in sorted order...
		for key in sorted(trunc.items(), key=lambda x: x[1]):
			if (rem == 0):
				break
			# distribute sliver of proportion to the app. key
			trunc[key[0]] += 1
			rem -= 1

	for key in trunc:
		trunc[key] = trunc[key] / 100

	return trunc

def vis_pos(filename, nlp):
	# opens the document info text file
	info = open("document_info.txt", "r")
	contents = info.read()
	info_dict = ast.literal_eval(contents)
	info.close()

	# creates the path to the correct folder
	folder_path = "./texts/" + filename
	pos_dict = {}
	pgs = info_dict[filename]["pgs"]

	# for each text...
	for i in range(pgs):
		# loads the text
		text_path = folder_path + "/content_" + str(i + 1) + ".txt"
		text = open(text_path, "r")
		text = text.read()

		# applies the pos_extractor to the text
		doc = nlp(text)
		tagged_text = [(w.text, w.tag_, w.pos_, w.lemma_, w.idx) for w in doc]
		
		# for each token...
		for token in tagged_text:
			# updates the count in the dict
			pos = token[2]
			if pos in pos_dict:
				pos_dict[pos] += 1
			else:
				pos_dict[pos] = 1

	# removes punctuation and spaces from the dictionary
	del pos_dict['PUNCT']
	del pos_dict['SPACE']

	# prints the results
	total = sum(pos_dict.values())
	print(filename + " POS counts:")
	print("Total: " + str(total))
	print(pos_dict)
	print('\n')

	# creates dictionary of proportions of POS in text
	pos_prop_dict = copy.deepcopy(pos_dict)
	for key in pos_prop_dict:
		pos_prop_dict[key] /= total

	# prints the results
	print(filename + " POS proportions:")
	print(pos_prop_dict)
	print('\n')

	# rounds the proportions using the largest remainder method
	trunc = roundy(pos_prop_dict)	

	return(pos_dict, trunc)


def vis_pos_all(nlp):
	# gets the list of documents
	docs = [x[0] for x in os.walk("./texts/")][1:]
	docs = [x.split('/')[-1] for x in docs]

	pos_counts = {}

	# for each document...
	for doc in docs:
		# updates overall dict
		res = vis_pos(doc, nlp)[0]
		pos_counts = {key: pos_counts.get(key, 0) + res.get(key, 0)
			for key in set(pos_counts.keys()) | set(res.keys())}

	# prints the results
	total = sum(pos_counts.values())
	print("Overall POS counts:")
	print("Total: " + str(total))
	print(pos_counts)
	print('\n')

	# creates dictionary of proportions of POS over all texts
	pos_prop_dict = copy.deepcopy(pos_counts)
	for key in pos_prop_dict:
		pos_prop_dict[key] /= total

	# prints the results
	print("Overall POS proportions:")
	print(pos_prop_dict)
	print('\n')

	# rounds the proportions using the largest remainder method
	trunc = roundy(pos_prop_dict)

	return (pos_counts, trunc)


if __name__ == '__main__':
	# establishes the argument scheme
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--document", required=True, help="name of book folder to be OCR'd; 'full' if all")
	ap.add_argument('-p', action='store_true', default=False, help="plot results")
	args = vars(ap.parse_args())

	# initializes the spacy pos model
	nlp = spacy.load('en_core_web_sm')

	inp = args["document"]

	# if the user specifies a doc...
	if (inp != "full"):
		# performs the calculations on only that document
		counts, props = vis_pos(inp, nlp)

	# else if the user does not specify a doc...
	elif (inp == "full"):
		# performs the calculations over all documents
		counts, props = vis_pos_all(nlp)

	# else, throws an error
	else:
		print("ERROR")

	# creates a plot for the data
	sort = {k: v for k, v in sorted(props.items(), key=lambda item: item[1], reverse=True)}
	labels = sort.keys()
	sizes = sort.values()

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=[str(round(x * 100)) + "%" for x in sizes], labeldistance=1.05)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	ax1.legend(labels, loc = "upper right", fontsize=5) 

	# creates the plot title
	if (inp == "full"):
		plt.title("Relative percentages of each POS in all documents")
	else:
		plt.title("Relative percentages of each POS in \n" + inp)

	# saves the plot
	plt.savefig('./figures/posize_' + inp + '.png')

	# if requested, shows the plot
	if (args["p"]):
		plt.show(block=True)

	# clears the plot
	plt.clf()


