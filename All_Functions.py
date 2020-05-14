# to do
# get special characters fixed: right now quotations and accent marks are not being cleaned correctly


# Imports
import requests
import time
# import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import csv
from nltk.corpus import stopwords
from collections import Counter
import glob
import os
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from cucco import Cucco
import seaborn as sns
import collections
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Variables / Parameters
male_keywords = ['hombre', 'padre', 'niño', 'niños', 'esposo', 'hombres', 'padres', 'esposos', 'masculina', 'masculino', 'marido']
female_keywords = ['mujer', 'niñas', 'niña', 'madre', 'mujeres', 'esposa', 'esposas', 'madres', 'femenino', 'femenina']
other_gender_keywords = ['género', 'adolescente', 'adulta']
M_migrant_keywords = ['hombre inmigrante', 'hombres inmigrantes', 'hombre migrante' 'hombre migrante',
                      'hombres migrantes', 'migración masculina', 'migraciones masculinas', 'migración de hombres']
F_migrant_keywords = ['mujer inmigrante', 'mujeres inmigrantes', 'mujer migrante', 'mujeres migrantes',
                      'migración feminina', 'migraciones feminina', 'migración de mujeres']
migrant_keywords = ['inmigrante', 'inmigrantes', 'migrantes', 'migrantes', 'migración', 'migraciones',
                    'solicitante de asilo', 'solicitantes de asilo', 'migratorio', 'migratoria', 'migratorios',
                    'migratorias', 'extranjero', 'extranjera', 'extranjeros', 'extranjeras', 'inmigración',
                    'inmigraciones', 'indocumentados', 'indocumentadas', 'indocumentado', 'indocumentada', 'emigrar']
# keyword lists in progress
quantity_keywords = ['número','reducir', 'número','cientos','centenar','medio','millones','doce']
childrenfamily_keywords = ['embarazada','embarazadas','niños','niñas','niña' ,'niño' ,'esposo','esposa' ,'cuidado', 'marido','ancianos','anciana' ,
'ancianas','anciano' ]

migrantCsvDirectory = 'C:/Users/khahn/PycharmProjects/HypothesisA/articleDB/migrants/migrants/' # get articles from migrant folder


def get_articles(directory):
    csvfiles = glob.glob(os.path.join(directory, '*.csv'))  # get the files in that folder
    csvcontent = []  # list that will contain the csv files
    csvColumns = []
    columnsList = []
    urlsList = []
    for elt in csvfiles:
        f = open(elt, 'r')
        csv_f = csv.reader(f)
        csvcontent.append(csv_f)
    # clean the articles and put them into one list
    for csvfile in csvcontent:  # reads the columns for each of the csv files
        for column in csvfile:
            csvColumns.append(column)
    for elt in csvColumns:  # makes each column a string in one list
        for i in elt:
            columnsList.append(i)
    while '' in columnsList:  # remove empty strings
        columnsList.remove('')
    totalElements = len(columnsList)
    for elt in columnsList:  # remove content that is not a url and remove repeated urls
        if elt.startswith('http') and elt not in urlsList:
            urlsList.append(elt)
    totalUnrepeatedElements = len(urlsList)
    print('There were', totalElements, 'elements orginally, but only', totalUnrepeatedElements, 'unrepeated urls total.')
    return urlsList


# Get website headline
# input: single url
# output: clean headline as a string NOT TOKENIZED
# TO DO: make it tokenized?? whats the difference in value?
# Note: h1 seems like it doesnt work as universally as 'title'
def get_page_h1(url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    headline = soup.find('h1').get_text().strip()
    return headline


def get_page_title(url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    headline = soup.find('title').get_text().strip()
    return headline


# Get website text
# input: single url
# output: list of lists which are tokenized sentences
# problems: with the test, has a bunch of empty lists at the end; not clean
def get_page_sentences(url):
    paragraphs_normalized = []
    normEsp = Cucco()
    norms = ['replace_punctuation', 'remove_extra_whitespaces']
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    paragraphs = soup.find_all('p')
    stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]
    for sentence in stripped_paragraph:
        paragraphs_normalized.append(normEsp.normalize(sentence, norms))
    return paragraphs_normalized


# Tokenize
# inputs: list of sentences as strings
# return: list of list of sentences which are tokenized
def get_token_sentences(sentence_list):
    return [word_tokenize(word) for word in sentence_list]


# Search for related words in specific (keyword) sentences
# inputs: list of sentences as a string, list of string of keywords
# Note: sentence_list should NOT be tokenized
# return:  list of related words as strings
def search_related_words(sentence_list, keyword_list):
    token_sentences, matched_sentences, related_words_list, lowered_sentences = ([] for i in range(4))
    new_stopwords = set(stopwords.words('spanish'))
    quotations = ['“', '”', 'así', 'hace', 'por', 'el', 'la', 'detenciã³n', 'copyright']
    new_stopwords.update(quotations)

    # lowercase
    for sentence in sentence_list:
        lowered_sentences.append(sentence.lower())
    # token sentences
    token_sentences = get_token_sentences(lowered_sentences)

    # get matched sentences
    for sentence in token_sentences:
        for keyword in keyword_list:
            if (keyword in sentence) and (sentence not in matched_sentences):
                matched_sentences.append(sentence)

    # get related words in matched sentences that are not initial keywords and stopwords
    for sentence in matched_sentences:
        for word in sentence:
            if (word not in new_stopwords) and (word not in keyword_list):
                related_words_list.append(word)
    return related_words_list


# Plot the frequent related words
# input: list of sentences, title of the plot
# output: plot of the most frequent related words
def plot_related_freq(text, title):
    counter = Counter(text)
    most = counter.most_common()
    x, y = [], []
    for word, count in most[:15]:
        x.append(word)
        y.append(count)
    sns.barplot(x=y, y=x, color='cyan').set_title(title)
    plt.show()


# Plot the frequent KEYWORD words
# input: list of sentences, list of keywords, title of the graph
# Note: list of sentences can be a list of strings, does not need to be tokenized
# output: plot of the most frequently appearing keywords
def plot_keyword_freq(sentence_list, keyword_list, title):
    matched_keywords = []
    for sentence in sentence_list:
        for word in keyword_list:
            if word in sentence:
                matched_keywords.append(word)
    counter = Counter(matched_keywords)
    most = counter.most_common()
    x, y = [], []
    for word, count in most[:15]:
        x.append(word)
        y.append(count)
    sns.barplot(x=y, y=x, color='cyan').set_title(title)
    plt.show()


# Count the number of keywords used in a list of sentences
# input: cleaned sentence list, keyword list, name of the keyword list
# output: a printed phrase saying the quantity of keywords found and a saved variable of the frequency
# to do: figure out how the double return thing works, make it so you dont have to input the name of the list
def count_freq_keywords(sentence_list, keyword_list, name_of_list):
    matched_keywords = []
    for sentence in sentence_list:
        for word in keyword_list:
            if word in sentence:
                matched_keywords.append(word)
    print('There are', len(matched_keywords), 'keywords present from', name_of_list)
    counter_keywords = Counter(matched_keywords)
    freq_keywords = counter_keywords.most_common()
    return freq_keywords


#  gets ngrams
# input: tokenized list of data, type of ngram
# output: readable ngrams
def extract_ngrams(data, num):
    n_grams = ngrams(data, num)
    return [' '.join(grams) for grams in n_grams]



# gets ngrams for a text
# input: list of lists of sentences, keywords to search, type of ngram
# output: 5 most common ngrams, list of all the ngrams
def load_ngrams(text, keywords, number):
    manyNgrams = []
    # to change back, switched cleanedText for matched_sentences
    for elt in text:
        getNgrams = extract_ngrams(elt, number)
        manyNgrams.append(getNgrams)
    print('There are', len(manyNgrams), 'elements in manyNgrams')
    keywordNgrams = []
    for i in manyNgrams:
        for gram in i:
            for keyword in keywords:
                if (keyword in gram) and (gram not in keywordNgrams):
                    keywordNgrams.append(gram)
    print('There are', len(keywordNgrams), 'elements in keywordNgrams')
    ngramFreq = collections.Counter(keywordNgrams)
    print(ngramFreq.most_common(5))
    return keywordNgrams
