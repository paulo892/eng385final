import re
import json
import math
import ast
import os
import argparse
import plotly.graph_objs as go
import text_statistics
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

NUMBER_OF_COLORS = 10

# Credit: https://towardsdatascience.com/color-identification-in-images-machine-learning-application-b26e770c4c71
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

if __name__ == '__main__':

    # establishes the argument scheme
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--document", required=True, help="name of book folder to be processed")
    ap.add_argument('-p', action='store_true', default=False, help="plot results")
    ap.add_argument('-c', '--colors', help="number of colors to track")

    args = vars(ap.parse_args())

    # opens the document info text file
    info = open("document_info.txt", "r")
    contents = info.read()
    info_dict = ast.literal_eval(contents)
    info.close()

    doc = args["document"]

    # overwrites color count if supplied
    NUMBER_OF_COLORS = int(args["colors"])

    # uses page numbers to create list
    page_nums = [x + 1 for x in range(info_dict[doc]['pgs'])]

    # for each page in the book...
    for pg in page_nums:
        # loads image
        image = cv2.imread('./documents/' + doc + "/content_" + str(pg) + ".png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # resizes image for processing
        modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
        modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)

        # initializes KMeans model for clustering
        clf = KMeans(n_clusters = NUMBER_OF_COLORS)
        labels = clf.fit_predict(modified_image)

        # counts the labels
        counts = Counter(labels)

        # gets the color centers
        center_colors = clf.cluster_centers_

        # gets ordered colors by iterating thru keys
        ordered_colors = [center_colors[i] for i in counts.keys()]
        hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
        rgb_colors = [ordered_colors[i] for i in counts.keys()]

        # plots pie if requested
        plt.figure(figsize = (8, 6))
        plt.title("Most common colors on page " + str(pg) + " of " + doc)
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        plt.savefig('./figures/' + doc + '/colors_across_text_' + str(pg) + '.png' )
        if args['p']:
            plt.show()
        plt.clf()
