import argparse
import os
import spacy
import ast
import copy 
import math
import matplotlib.pyplot as plt

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

	# removes punctuation from the dictionary
	del pos_dict['PUNCT']

	# prints the results
	total = sum(pos_dict.values())
	print(filename + " word counts:")
	print("Overall: " + str(total))
	print("By POS:")
	print(pos_dict)

	# creates dictionary of proportions of POS in text
	pos_prop_dict = copy.deepcopy(pos_dict)
	for key in pos_prop_dict:
		pos_prop_dict[key] /= total

	# prints the results
	print(filename + " POS proportions:")
	print(pos_prop_dict)

	## rounds the proportions using the largest remainder method

	# truncates each of the proportions to hundredths place
	trunc = copy.deepcopy(pos_prop_dict)
	for key in trunc:
		trunc[key] = math.trunc(trunc[key] * 100) / 100

	# sums the values and subtracts from 1
	diff = (1 - sum(trunc.values()))
	print(sum(trunc.values()))
	print(diff)

	# rounds the difference off
	diff = math.trunc(round(diff * 100)) / 100

	rem = int(diff * 100)
	for key in trunc:
		trunc[key] = trunc[key] * 100
	print("hello" + str(pos_dict))
	# while int > 0...
	while (rem > 0):
		# for each key, in sorted order...
		for key in sorted(trunc.items(), key=lambda x: x[1]):
			print(key)
			if (rem == 0):
				break
			# distribute sliver of proportion to the app. key
			trunc[key[0]] += 1
			rem -= 1

	for key in trunc:
		trunc[key] = trunc[key] / 100

	# print results
	# prints the results
	print(filename + " POS proportions (truncated):")
	print(trunc)

	print("hello" + str(pos_dict))
	return(pos_dict, trunc)



def vis_pos_all(nlp):
	print("Goodbye")
	# TODO

if __name__ == '__main__':
	# establishes the argument scheme
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", required=True, help="'full' if want to perform visualization over all documents, name of specific document folder otherwise")
	args = vars(ap.parse_args())

	# initializes the spacy pos model
	nlp = spacy.load('en_core_web_sm')

	inp = args["input"]

	# if the user specifies a doc...
	if (inp != "full"):
		# performs the visualization on only that document
		counts, props = vis_pos(inp, nlp)
		print(counts)
		print(props)

		# displays the results in a pie chart
		labels = props.keys()
		sizes = props.values()

		sort = {k: v for k, v in sorted(props.items(), key=lambda item: item[1], reverse=True)}
		labels = sort.keys()
		print(sort)
		sizes = sort.values()
		print(sizes)
		#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

		fig1, ax1 = plt.subplots()
		ax1.pie(sizes, labels=[str(round(x * 100)) + "%" for x in sizes], labeldistance=1.05)
		ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		ax1.legend(labels, loc = "upper right", fontsize=5) 
		plt.title("Relative percentages of each POS in \n" + inp)


		plt.show()

	# else if the user does not specify a doc...
	elif (inp == "full"):
		vis_pos_all(nlp)

