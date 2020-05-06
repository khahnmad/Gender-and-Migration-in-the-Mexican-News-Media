# Imports
import requests
import time
# import httplib2
from bs4 import BeautifulSoup, SoupStrainer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from cucco import Cucco
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Variables / Parameters
male_keywords = ['hombre', 'padre', 'niño', 'niños', 'esposo', 'hombres', 'padres', 'esposos', 'masculina', 'masculino']
female_keywords = ['mujer', 'niñas', 'niña', 'madre', 'mujeres', 'esposa', 'esposas', 'madres', 'femenino', 'femenina']
other_gender_keywords = ['género', 'adolescente', 'adulta']
M_migrant_keywords = ['hombre inmigrante', 'hombres inmigrantes', 'hombre migrante' 'hombre migrante',
                      'hombres migrantes', 'migración masculina', 'migraciones masculinas', 'migración de hombres']
F_migrant_keywords = ['mujer inmigrante', 'mujeres inmigrantes', 'mujer migrante', 'mujeres migrantes',
                      'migración feminina', 'migraciones feminina', 'migración de mujeres']
migrant_keywords = ['inmigrante', 'inmigrantes', 'migrantes', 'migrantes', 'migración', 'migraciones',
                    'solicitante de asilo', 'solicitantes de asilo', 'migratorio', 'migratoria', 'migratorios',
                    'migratorias', 'extranjero', 'extranjera', 'extranjeros', 'extranjeras', 'inmigración',
                    'inmigraciones', 'indocumentados', 'indocumentadas', 'indocumentado', 'indocumentada']


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
