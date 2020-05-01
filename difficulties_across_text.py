import re
import json
import math
import ast
import os
import argparse
import plotly.graph_objs as go
import text_statistics
import matplotlib.pyplot as plt


if __name__ == '__main__':

    # establishes the argument scheme
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--document", required=True, help="name of book folder to be processed")
    ap.add_argument('-p', action='store_true', default=False, help="plot results")
    ap.add_argument('-s', action='store_true', default=False, help="include if semi-colons should be considered sentence-terminating punctuation")

    args = vars(ap.parse_args())

    # opens the document info text file
    info = open("document_info.txt", "r")
    contents = info.read()
    info_dict = ast.literal_eval(contents)
    info.close()

    # extracts difficulty metrics
    rand_doc = next(iter(info_dict.keys()))
    metrics = info_dict[rand_doc]['stats'].keys()
    metrics_across_pages = {}

    doc = args["document"]
    sc = args['s']

    # uses page numbers to create list
    page_nums = [x + 1 for x in range(info_dict[doc]['pgs'])]

    # for each page in the book...
    for pg in page_nums:
        # loads the text
        text = open('./texts/' + doc + "/content_" + str(pg) + ".txt", "r")
        text = text.read()
        text = text.strip()

        # derives metrics for text
        mets = text_statistics.statisticize(text, sc)

        # for each metric...
        for met in metrics:
            if met == 'doc':
                continue
            # appends the value for that page to corr. list
            if met not in metrics_across_pages:
                metrics_across_pages[met] = []
                metrics_across_pages[met].append(mets[met])
            else:
                metrics_across_pages[met].append(mets[met])

    # plots results in individual graphs
    for key in metrics_across_pages:
        ax = plt.gca()
        ax.plot(page_nums, metrics_across_pages[key], label=key)
        plt.xlabel('Page of work')
        plt.ylabel(key + ' value')
        plt.title('Magnitude of ' + key + ' by page of ' + doc)
        plt.axis('tight')
        plt.savefig('./figures/' + doc + '/difficulties_across_text_' + key + '.png')
        if args['p']:
            plt.show(block=True)
        plt.clf()
