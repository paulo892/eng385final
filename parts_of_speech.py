import argparse
import os
import spacy
import ast
import copy 
import math
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import json

COLOR_DICT = {
	'ADJ': 'b', 'ADP': 'g', 'CCONJ': 'r', 'CONJ': 'c', 
	'AUX': 'm', 'ADV': 'y', 'DET': 'k', 'INTJ': 'tab:blue', 
	'NOUN': 'tab:orange', 'NUM': 'tab:green', 
	'PART': 'tab:purple', 'PRON': 'tab:pink', 
	'PROPN': 'tab:gray', 'PUNCT': 'darkred', 
	'SCONJ': 'gold', 'SYM': 'tab:red', 
	'VERB': 'tab:brown', 'X': 'limegreen', 
	'SPACE': 'darkslategrey'
}

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

def create_plot(props, model):
	# creates a plot for the data
	sort = {k: v for k, v in sorted(props.items(), key=lambda item: item[1], reverse=True)}
	print('efojsfejse')
	print(sort)
	labels = sort.keys()
	sizes = sort.values()

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=[str(round(x * 100)) + "%" for x in sizes], colors=[COLOR_DICT[x] for x in labels], labeldistance=1.05)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	ax1.legend(labels, loc = "upper right", fontsize=5) 

	# creates the plot title
	if (inp == "full"):
		plt.title("Relative percentages of each POS in all documents")
	else:
		plt.title("Relative percentages of each POS in \n" + model)

	# saves the plot
	plt.savefig('./figures/posize_' + model + '.png')

	# clears the plot
	plt.clf()
	plt.cla()
	plt.close()

def display_plot(path):
	# loads image
	img = mpimg.imread(path)
	imgplot = plt.imshow(img)
	plt.axis('off')
	plt.show()


# TODO - Get this working!
def display_plots():
	# gets images
	images = os.listdir('./figures/')
	img_count = len(images)

	# adjusts image count
	if ('posize_each.png' in images):
		img_count -= 1
	if ('.DS_Store' in images):
		img_count -= 1

	# sets parameters
	fig = plt.figure(figsize=(10, 5))
	columns = 2
	rows = np.ceil(img_count / 2)

	for x, i in enumerate(images):
		if i == 'posize_each.png' or i == '.DS_Store':
			continue
		path =  os.path.join("./figures/",i)
		img = plt.imread(path)
		fig.add_subplot(rows, columns, x)
		plt.imshow(img, aspect='auto')
		plt.axis('off')

	plt.savefig('./figures/posize_each.png')
	plt.show()

def update_doc(doc, props):
	## updates document_info.txt with POS proportions

	# opens the document_info.txt file and reads contents
	contents = None
	with open("document_info.txt", "r") as jsonFile:
		contents = json.load(jsonFile)

	# updates the document POSs
	contents[doc]['POS_props'] = props

	with open("document_info.txt", "w") as jsonFile:
		json.dump(contents, jsonFile)

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
	if (inp != "full" and inp != "each"):
		# performs the calculations on only that document
		counts, props = vis_pos(inp, nlp)

		# creates plot
		create_plot(props, inp)

		# displays plot if requested
		if args['p']:
			display_plot('./figures/posize_' + inp + '.png')

		# updates document info doc
		update_doc(inp, props)

	# else if the user specifies "each"...
	elif (inp == "each"):
		# gets the list of documents
		docs = [x[0] for x in os.walk("./documents/")][1:]
		docs = [x.split('/')[-1] for x in docs]

		# for each document...
		for doc in docs:
			# performs the calculations on only that document
			counts, props = vis_pos(doc, nlp)

			# creates plot
			create_plot(props, doc)

			# updates document info doc
			update_doc(doc, props)

		# displays plots if requested
		if args['p']:
			display_plots()

	# else if the user specifies "full"...
	elif (inp == "full"):
		# performs the calculations over all documents
		counts, props = vis_pos_all(nlp)

		# creates plot
		create_plot(props, inp)

		# displays plot if requested
		if args['p']:
			display_plot('./figures/posize_' + inp + '.png')

		# updates document info doc
		update_doc(inp, props)

	# else, throws an error
	else:
		print("Invalid input.")

	

	


