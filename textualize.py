from PIL import Image
import pytesseract
import argparse
import cv2
import os
import ast

def textualize(doc):
	image_folder_path = "./documents/" + doc
	text_folder_path = "./texts/" + doc

	# creates directory for textualized book
	if not os.path.exists(text_folder_path):
		try:
			os.mkdir(text_folder_path)
		except OSError:
			print ("Creation of the directory %s failed" % text_folder_path)
		else:
			print ("Successfully created the directory %s " % text_folder_path)

	# for each page in the document...
	pgs = info_dict[doc]["pgs"]
	for i in range(pgs):

		# saves the image in an object
		image_path = image_folder_path + "/content_" + str(i + 1) + ".png"
		img = cv2.imread(image_path)

		# creates a gray-scale version of the image for model application
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		filename = "{}.png".format(os.getpid())
		cv2.imwrite(filename, gray_img)

		# extracts text and deletes the file
		text = pytesseract.image_to_string(Image.open(filename))
		os.remove(filename)

		filename = text_folder_path + "/content_" + str(i + 1) + ".txt"

		# deletes existing file if exists
		if os.path.exists(filename):
			os.remove(filename)

		# saves text
		f = open(filename,"w+")
		f.write(text)
		f.close()

if __name__ == '__main__':
	# establishes the argument scheme
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--document", required=True, help="name of book folder to be OCR'd; 'full' if all")
	ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
	args = vars(ap.parse_args())

	# opens the document info text file
	info = open("document_info.txt", "r")
	contents = info.read()
	info_dict = ast.literal_eval(contents)
	info.close()

	doc = args["document"]

	# if document name specified, textualize document
	if doc != "full":
		textualize(doc)
	# else, textualize all documents
	else:
		# gets the list of documents
		docs = [x[0] for x in os.walk("./documents/")][1:]
		docs = [x.split('/')[-1] for x in docs]

		for doc in docs:
			textualize(doc)
		
