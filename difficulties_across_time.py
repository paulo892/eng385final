import re
import json
import math
import ast
import os
import argparse
import plotly.graph_objs as go
import text_statistics
import matplotlib.pyplot as plt
import text_statistics


if __name__ == '__main__':

    # establishes the argument scheme
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--metric", required=True, help="difficulty metric to use; 'each' for each of them")
    ap.add_argument('-s', action='store_true', default=False, help="include if semi-colons should be considered sentence-terminating punctuation")
    ap.add_argument('-p', action='store_true', default=False, help="plot results")

    args = vars(ap.parse_args())

    # opens the document info text file
    info = open("document_info.txt", "r")
    contents = info.read()
    info_dict = ast.literal_eval(contents)
    info.close()

    metric = args['metric']
    sc = args['s']

    # if metric specified...
    if metric != 'each':
        # only considers that metric
        metrics = [metric]

    # else, will consider all metrics
    else:
        rand_doc = next(iter(info_dict.keys()))
        metrics = info_dict[rand_doc]['stats'].keys()

    pairs = []
    # for each document...
    for doc in info_dict:
        # creates the path to the correct folder
        folder_path = "./texts/" + doc
        print(doc)
        pgs = info_dict[doc]["pgs"]

        text_grl = ""

        # creates general text for analysis
        for i in range(pgs):
            text = open(folder_path + "/content_" + str(i + 1) + ".txt", "r")
            text = text.read()
            text = text.strip()
            text_grl = text_grl + text + ". "

        # pulls metrics from text
        stats = text_statistics.statisticize(text_grl, sc)

        # extracts publication year
        yr = int(info_dict[doc]['pub_date'])

        # saves data
        pairs.append((doc, yr, stats))

    year_values = {}
    # aggregates entries within each year
    for entry in pairs:
        # adds year values to dict...
        if entry[1] not in year_values:
            year_values[entry[1]] = [entry[2]]
        else:
            year_values[entry[1]].append(entry[2])

    # averages values within each year
    for year in year_values:
        vals = year_values[year]
        dict_sum = {}
        for dic in vals:
            dict_sum.update(dic)
        for k in dic:
            dic[k] = dic[k] / len(vals)
        year_values[year] = dic

    # creates new pairs object
    pairs = []
    for year in year_values:
        pairs.append((year, year_values[year]))

    # sorts the entries
    pairs.sort(key=lambda x:x[0])

    # for each requested metric...
    for met in metrics:
        if met == 'doc':
            continue
        ax = plt.gca()
        ax.plot([x[0] for x in pairs], [x[1][met] for x in pairs], label=met)
        plt.xlabel('Publication year')
        plt.ylabel(met + ' value')
        plt.title('Magnitude of ' + met + ' by work publication year')
        plt.axis('tight')
        plt.savefig('./figures/' + 'full' + '/difficulties_across_time_' + met + '.png')
        if args['p']:
            plt.show(block=True)
        plt.clf()