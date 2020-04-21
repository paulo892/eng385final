import os
import numpy as np
import argparse
import ast
import spacy
from spacy import displacy
import matplotlib.pyplot as plt

if __name__ == '__main__':
	# establishes argument scheme
	ap = argparse.ArgumentParser()
	ap.add_argument("-t", "--type", required=True, help="kind of display ('figures' - all figures, 'deps' - dependencies)")
	ap.add_argument('-d', "--document", help="if -t = 'deps', file name to be displayed")
	args = vars(ap.parse_args())

	form = args['type']

	# opens the document info text file
	info = open("document_info.txt", "r")
	contents = info.read()
	info_dict = ast.literal_eval(contents)
	info.close()

	# displays figures in a grid
	if form == "figures":
		directory = "./figures/"
		images = os.listdir(directory)

		fig = plt.figure(figsize=(10, 10))
		columns = 2
		rows = np.ceil(len(images))

		for x, i in enumerate(images):
		    path =  os.path.join("./figures/",i)
		    img = plt.imread(path)
		    fig.add_subplot(rows, columns, x+1)
		    plt.imshow(img)
		plt.show()

	# displays dependencies of argument text
	if form == "deps":
		# retrieves and collates texts
		doc = args['document']
		pgs = info_dict[doc]["pgs"]
		text_folder_path = "./texts/" + doc

		text_grl = ""

		for i in range(pgs):
			text = open(text_folder_path + "/content_" + str(i + 1) + ".txt", "r")
			text = text.read()
			text = text.strip()
			text_grl = text_grl + text + ". "

		# loads and applies spacy model
		nlp = spacy.load("en_core_web_sm")
		doc = nlp(text)

		# displays the dependencies
		displacy.serve(doc, style="dep")



