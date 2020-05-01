import re
import json
import math
import ast
import os
import argparse
import spacy
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import plotly.graph_objs as go
import text_statistics
import matplotlib.pyplot as plt


if __name__ == '__main__':

    # establishes the argument scheme
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--document", required=True, help="name of book folder to be processed; 'full' if all")
    ap.add_argument('-p', action='store_true', default=False, help="plot results")
    ap.add_argument('-t', required=True, help="part of speech to be clouded: 'NOUN', 'ADJ', 'VERB'")

    args = vars(ap.parse_args())

    # opens the document info text file
    info = open("document_info.txt", "r")
    contents = info.read()
    info_dict = ast.literal_eval(contents)
    info.close()

    # initializes the spacy pos model
    nlp = spacy.load('en_core_web_sm')

    doc = args["document"]
    t = args['t']

    # if document name specified, clouds document
    if doc != "full" and doc != "each":
        # creates the path to the correct folder
        folder_path = "./texts/" + doc
        pgs = info_dict[doc]["pgs"]

        text_grl = ""

        # creates general text for analysis
        for i in range(pgs):
            text = open(folder_path + "/content_" + str(i + 1) + ".txt", "r")
            text = text.read()
            text = text.strip()
            text_grl = text_grl + text + ". "

        # applies model to text
        pos_text = nlp(text_grl)
        tagged_text = [(w.text, w.pos_) for w in pos_text]

        tokens = []
        # filters list on POS desired
        for pair in tagged_text:
            if pair[1] == t:
                tokens.append(pair)

        # creates text for clouding
        cloudable = ""
        for pair in tokens:
            cloudable = cloudable + pair[0] + " "

        # creates wordcloud
        print(cloudable)
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", relative_scaling=1).generate(cloudable)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('./figures/' + doc + '/pos_word_cloud_' + t + '.png')
        if (args['p']):
            plt.show()

    # if 'full' clouds all documents
    elif doc == "full":
        # gets the list of documents
        docs = [x[0] for x in os.walk("./texts/")][1:]
        docs = [x.split('/')[-1] for x in docs]

        text_grl = ""
        # for each doc...
        for name in docs:
            # creates the path to the correct folder
            folder_path = "./texts/" + name
            pgs = info_dict[name]["pgs"]

            # creates general text for analysis
            for i in range(pgs):
                text = open(folder_path + "/content_" + str(i + 1) + ".txt", "r")
                text = text.read()
                text = text.strip()
                text_grl = text_grl + text + " "

        # applies model to text
        pos_text = nlp(text_grl)
        tagged_text = [(w.text, w.pos_) for w in pos_text]

        tokens = []
        # filters list on POS desired
        for pair in tagged_text:
            if pair[1] == t:
                tokens.append(pair)

        # creates text for clouding
        cloudable = ""
        for pair in tokens:
            cloudable = cloudable + pair[0] + " "

        # creates wordcloud
        print(cloudable)
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", relative_scaling=1).generate(cloudable)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('./figures/' + doc + '/pos_word_cloud_' + t + '.png')
        if (args['p']):
            plt.show()

    # if 'each' clouds each document
    elif doc == 'each':
        # gets the list of documents
        docs = [x[0] for x in os.walk("./texts/")][1:]
        docs = [x.split('/')[-1] for x in docs]

        text_grl = ""
        # for each doc...
        for name in docs:
            # creates the path to the correct folder
            folder_path = "./texts/" + name
            pgs = info_dict[name]["pgs"]

            # creates general text for analysis
            for i in range(pgs):
                text = open(folder_path + "/content_" + str(i + 1) + ".txt", "r")
                text = text.read()
                text = text.strip()
                text_grl = text_grl + text + " "

            # applies model to text
            pos_text = nlp(text_grl)
            tagged_text = [(w.text, w.pos_) for w in pos_text]

            tokens = []
            # filters list on POS desired
            for pair in tagged_text:
                if pair[1] == t:
                    tokens.append(pair)

            # creates text for clouding
            cloudable = ""
            for pair in tokens:
                cloudable = cloudable + pair[0] + " "

            # creates wordcloud
            print(cloudable)
            wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", relative_scaling=1).generate(cloudable)
            plt.figure()
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.savefig('./figures/' + name + '/pos_word_cloud_' + t + '.png')
            if (args['p']):
                plt.show()