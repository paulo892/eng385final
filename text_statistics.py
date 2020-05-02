import re
import json
import math
import ast
import os
import argparse
import plotly.graph_objs as go

def syllables(word):
    # Count the syllables in the word.
    syllables = 0
    for i in range(len(word)):

       # If the first letter in the word is a vowel then it is a syllable.
       if i == 0 and word[i] in "aeiouy" :
          syllables = syllables + 1

       # Else if the previous letter is not a vowel.
       elif word[i - 1] not in "aeiouy" :

          # If it is no the last letter in the word and it is a vowel.
          if i < len(word) - 1 and word[i] in "aeiouy" :
             syllables = syllables + 1

          # Else if it is the last letter and it is a vowel that is not e.
          elif i == len(word) - 1 and word[i] in "aiouy" :
             syllables = syllables + 1

    # Adjust syllables from 0 to 1.
    if len(word) > 0 and syllables == 0 :
       syllables == 0
       syllables = 1

    return syllables


def statisticize(text, sc):
    features = {}

    # adjust text in various ways
    textA = re.sub('\.\.+', '\.', text)

    # calculates number of sentences
    if (sc):
        sentences = re.split('\.|!|;', textA)
    else:
        sentences = re.split('\.|!', textA)

    sentencesA = []
    for sen in sentences:
        if re.search('\s\w+\s', sen):
            sentencesA.append(sen)
    num_sentences = len(sentencesA)
    features['sentences'] = num_sentences

    # calculates number of words
    words = []
    num_words = 0
    for sen in sentencesA:
        words.extend(re.split('\s+', sen))

    # trims each word and removes non-words and non-alphanumerics
    wordsA = []
    for word in words:
        word = word.strip()
        if re.search('\w+', word):
            wordsA.append(re.sub(r'\W+', '', word))
    words = wordsA

    num_words = len(words)
    features['words'] = num_words

    # calculates number of syllables
    num_syllables = 0
    for word in words:
        num_syllables += syllables(word)
    features['syllables'] = num_syllables

    # calculates number of letters
    num_letters = 0
    for word in words:
        num_letters += len(word)
    features['letters'] = num_letters

    # calculates number of unique words
    words_upper = [x.upper() for x in words]
    words_set = set(words_upper)
    num_unique_words = len(words_set)
    features['unique_words'] = num_unique_words

    # calculates type-token ratio
    ttr = num_unique_words / num_words
    features['ttr'] = ttr

    # calculates flesch reading ease index
    flesch = 206.835 - (84.6) * (num_syllables/num_words) - (1.015) * (num_words/num_sentences)
    features['flesh-adap'] = flesch

    # calculates Coleman Liau
    coleman_liau = 5.88 * num_letters / num_words - 29.6 * num_sentences / num_words - 15.8
    features['coleman'] = coleman_liau

    # calculates Flesch Kincaid
    flesch_kincaid = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59
    features['flesch-grade'] = flesch_kincaid

    # calculates Automated Readability Index
    ari = 6.286 * num_letters / num_words + 0.927 * num_words / num_sentences - 36.551
    features['ari'] = ari


    # calculates average number of letters per word
    avg_letters_per_word = num_letters / num_words
    features['alw'] = avg_letters_per_word

    # returns dummy dictionary
    return features

def plot(stats_dict, headers):
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white' 

    docs = stats_dict.keys()
    #[stats_dict[x][headers[0]] for x in docs]
    temp = [[round(stats_dict[x][headers[y]], 2) if not isinstance(stats_dict[x][headers[y]], str) else stats_dict[x][headers[y]] for x in docs] for y in range(len(headers))]


    fig = go.Figure(data=[go.Table(
        header=dict(values=['<b>' + str(x) + '</b>' for x in headers],
                       line = dict(color = '#506784'),
                    fill = dict(color = headerColor),
                    align = ['left','center'],
                    font = dict(color = 'white', size = 12)),
        cells=dict(values= temp,
          line = dict(color = '#506784'),
        fill = dict(color = [rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]),
        align = ['left', 'center'],
        font = dict(color = '#506784', size = 11))
    )])
    fig.show()

def update_doc(dic):
    # opens the document_info.txt file and reads contents
    contents = None
    with open("document_info.txt", "r") as jsonFile:
        contents = json.load(jsonFile)

    # for each document...
    for doc in dic:
        # updates the stats
        contents[doc]['stats'] = dic[doc]

    # updates document
    with open("document_info.txt", "w") as jsonFile:
        json.dump(contents, jsonFile)

if __name__ == '__main__':

    # establishes the argument scheme
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--document", required=True, help="name of book folder to be OCR'd; 'each' if all")
    ap.add_argument('-s', action='store_true', default=False, help="include if semi-colons should be considered sentence-terminating punctuation")
    args = vars(ap.parse_args())

    # opens the document info text file
    info = open("document_info.txt", "r")
    contents = info.read()
    info_dict = ast.literal_eval(contents)
    info.close()

    doc = args["document"]
    sc = args["s"]
    headers = None

    # if document name specified, statisticizes document
    if doc != "each":
        stats_dict = {}

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

        # pulls metrics from text
        temp = statisticize(text_grl, sc)

        temp['doc'] = doc
        stats_dict[doc] = temp
        headers = stats_dict[doc].keys()

    # else, statisticizes all documents
    else:
        stats_dict = {}

        # gets the list of documents
        docs = [x[0] for x in os.walk("./texts/")][1:]
        docs = [x.split('/')[-1] for x in docs]

        # for each document...
        for doc in docs:
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

            # pulls metrics from text
            temp = statisticize(text_grl, sc)

            temp['doc'] = doc
            stats_dict[doc] = temp

            if headers is None:
                headers = stats_dict[doc].keys()

    # gets the headers
    headers = list(headers)

    # reorganizes the 'document' header
    headers.insert(0, headers.pop(headers.index('doc')))

    print(stats_dict)
    # updates document info doc
    update_doc(stats_dict)

    # plots the results
    plot(stats_dict, list(headers))