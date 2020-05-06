# To do
# expand the articles used, count the gender article databases
# is there any real difference between this and the function in all_function?


# Imports
import csv
from nltk.corpus import stopwords
import All_Functions as af
from collections import Counter
import glob
import os
import seaborn as sns
import matplotlib.pyplot as plt

# open the articles
csvdirectory = 'C:/Users/khahn/PycharmProjects/HypothesisA/articleDB/migrants/migrants/' # get articles from migrant folder
csvfiles = glob.glob(os.path.join(csvdirectory, '*.csv')) # get the files in that folder
csvcontent = [] # list that will contain the csv files
for elt in csvfiles:
    f = open(elt, 'r')
    csv_f = csv.reader(f)
    csvcontent.append(csv_f)
print('Opened the csv files')


# clean the articles and put them into one list
csvColumns = []
for csvfile in csvcontent: # reads the columns for the csv files
    for column in csvfile:
        csvColumns.append(column)
columnsList = []
for elt in csvColumns: # makes each element a string in one list
    for i in elt:
        columnsList.append(i)
while '' in columnsList: # remove empty strings
    columnsList.remove('')
urlsList = []
for elt in columnsList: # remove content that is not a url
    if elt.startswith('http') and elt not in urlsList:
        urlsList.append(elt)
print('There are', len(urlsList), 'urls in Urls List')


# get text and format it
listsOfSentences = []
for url in urlsList:
    text = af.get_page_sentences(url) # gets stripped p tags from each url
    listsOfSentences.append(text)
print('There are', len(listsOfSentences), 'lists of sentences in the variable listsOfSentences')
one_list_sentences = []
for elt in listsOfSentences: # make it just one list of all the strings
    for i in elt:
        one_list_sentences.append(i)
print('There are ', len(one_list_sentences), 'sentences in the list of sentences')

# Count the frequency of the different keywords
# Clean the text
new_stopwords = set(stopwords.words('spanish'))
quotations = ['“', '”', 'así', 'hace', 'por', 'el', 'la','detenciã³n','copyright']
all_text = []
lowered_sentences = []
new_stopwords.update(quotations)
for sentence in one_list_sentences: # make all letters lowercase
    lowered_sentences.append(sentence.lower())
token_sentences = af.get_token_sentences(lowered_sentences) # tokenize sentences
for sentence in token_sentences:
    for word in sentence:
        if word not in new_stopwords:
            all_text.append(word)
print('There are ', len(all_text), 'words in the variable all_text')
# to do: make this into a loop
freq_male_kws = af.count_freq_keywords(all_text, af.male_keywords, 'Male Keywords')
freq_female_kws = af.count_freq_keywords(all_text, af.female_keywords, 'Female keywords')
freq_other_kws = af.count_freq_keywords(all_text, af.other_gender_keywords, 'Other gender keywords')
print('Male:', freq_male_kws)
# note that padres probably almost always is referring to 'parents' and not 'fathers'
print('Female:', freq_female_kws)
print('Other gender:', freq_other_kws)


x, y, = ([] for i in range(2))
all_freq = [freq_female_kws, freq_male_kws]
for frequencyList in all_freq:
    for word, count in frequencyList:
        x.append(word)
        y.append(count)
sns.barplot(x=y, y=x, color='cyan').set_title('Most Common Keywords')
plt.show()
