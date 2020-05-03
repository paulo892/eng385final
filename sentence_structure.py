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
	ap.add_argument('-d', "--document", help="text whose sentence structure to display")
	args = vars(ap.parse_args())

	# opens the document info text file
	info = open("document_info.txt", "r")
	contents = info.read()
	info_dict = ast.literal_eval(contents)
	info.close()

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
	doc.user_data["title"] = "Sentence structures for " + str(doc)
	displacy.serve(doc, style="dep")



