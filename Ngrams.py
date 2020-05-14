# To do
# make a plot of the n grams
# could then do something about what part of speech falls before and after the female or male gendered words d
# sort the bngrams alphabetically


# imports
import collections
from nltk.corpus import stopwords
import All_Functions as af
import csv
from collections import Counter


# Variables
unnecessarywords = ['copyright', 'tweets', 'inscribirte', 'textjavascript', 'press','googletagcmdpushfunction']
startswith_migrantkeywords = ['inmigrante', 'migrante', 'migración', 'solicitante de asilo', 'migratorio', 'migratoria',
                              'extranjero', 'extranjera', 'inmigración','indocumentado', 'indocumentada']
startwith_male_keywords = ['hombre', 'padre', 'niño',  'esposo', 'masculina', 'masculino', 'marido']
startswith_female_keywords = ['mujer', 'niña', 'madre', 'mujer', 'esposa', 'femenino', 'femenina']


# Functions

# gets ngrams from a text that start with a given keyword
# input: clean, tokenized list of lists of strings; the keyword; the size of the ngram
# output: prints the 5 most common ngrams, returns uncounted ngrams
def load_ngrams_onekeywordfirst(text, keyword, number):
    manyNgrams = []
    # to change back, switched cleanedText for matched_sentences
    for elt in text:
        getNgrams = af.extract_ngrams(elt, number)
        manyNgrams.append(getNgrams)
    keywordfirst = []
    for i in manyNgrams:
        for gram in i:
            if gram.startswith(keyword): #and (gram not in keywordfirst):
                keywordfirst.append(gram)
    keywordfirstFreq = collections.Counter(keywordfirst)
    print(keywordfirstFreq.most_common(5))
    return keywordfirst


# gets all ngrams that start with a list of keywords
# input: list of lists of strings; list of keywords; size of ngram
# output: prints the 5 most common ngrams, returns uncounted ngrams
def load_ngrams_allkeywordsfirst(text, keywords, number):
    manyNgrams = []
    keywordfirst = []
    for elt in text:
        getNgrams = af.extract_ngrams(elt, number)
        manyNgrams.append(getNgrams)
    for i in manyNgrams:
        for gram in i:
            for keyword in keywords:
                if gram.startswith(keyword): # and gram not in keywordfirst:
                    keywordfirst.append(gram)
    keywordfirstFreq = collections.Counter(keywordfirst)
    print(keywordfirstFreq.most_common(5))
    return keywordfirst


# saves ngrams to a csv file
# input: list of lists of ngrams; name of the file; keyword the file is based on
# output: a csv file with rows of the ngrams 
def save_keywordfirst(text, name, keyword):
    loc_zero, loc_one, loc_two= ([] for i in range(3))
    for gram in text:
        splitstring = gram.split()
        loc_zero.append(splitstring[0])
        loc_one.append(splitstring[1])
        loc_two.append(splitstring[2])

    with open(name, mode='w') as ngram_file:
        ngram_writer = csv.writer(ngram_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        ngram_writer.writerow(keyword)
        for i in range(len(loc_one)):
            plusone = i + 1
            # print(plusone, loc_zero[i], loc_one[i], loc_two[i])
            aRow = [plusone, loc_zero[i], loc_one[i], loc_two[i]]
            ngram_writer.writerow(aRow)
    ngram_file.close()

# open the articles
urlList = af.get_articles(af.migrantCsvDirectory)


# Get text and convert it to one list of strings that contain the sentences
listsOfSentences = []
for url in urlList:
    sentences = af.get_page_sentences(url)  # gets stripped p tags from each url
    listsOfSentences.append(sentences)
print('There are', len(listsOfSentences), 'lists of sentences in the variable listsOfSentences')
one_list_sentences = []
for elt in listsOfSentences:  # make it just one list of all the strings
    for i in elt:
        one_list_sentences.append(i)


# Clean the sentences
new_stopwords = set(stopwords.words('spanish'))
quotations = ['“', '”', 'así', 'hace', 'por', 'el', 'la']
new_stopwords.update(quotations)
cleanedText, lowered_sentences, listCleanSentences = ([] for i in range(3))
for sentence in one_list_sentences:  # make all letters lowercase
    lowered_sentences.append(sentence.lower())
token_sentences = af.get_token_sentences(lowered_sentences) # tokenize sentences
print('There are ', len(token_sentences), 'elements in token sentences')
for i in token_sentences:
    for word in i:
        if word in unnecessarywords:
            token_sentences.remove(i)
manyrepeatssentences = []
for i in token_sentences:
    count = token_sentences.count(i)
    if count >= 3 and i not in manyrepeatssentences:
        manyrepeatssentences.append(i)
print('There are ', len(manyrepeatssentences), 'elements in many repeat sentences')
# print('Many Repeat Sentences:', manyrepeatssentences)
for i in token_sentences:
    if i in manyrepeatssentences:
        token_sentences.remove(i)
print('There are ', len(token_sentences), 'elements in token sentences')


duplicateSentences = [] # Not sure if this really needs to be here anymore
for i in token_sentences:
    count = token_sentences.count(i)
    if count > 1:
        # print(i, count)
        duplicateSentences.append(i)
print('There are ', len(duplicateSentences), 'duplicate sentences')


for sentence in token_sentences:
    clean_sentence = []
    for word in sentence:
        if word not in new_stopwords:
            clean_sentence.append(word)
    listCleanSentences.append(clean_sentence)
print('There are', len(listCleanSentences), 'elements in listCleanSentences')


# # get ngrams from the text based on the different keyword lists
# migrantNgrams = af.load_ngrams(listCleanSentences, af.migrant_keywords, 3) # 770 keyword ngrams
# print('Migrant ngrams', migrantNgrams)
# f_ngrams = af.load_ngrams(cleanedText, af.female_keywords, 3)
# print('F ngrams', f_ngrams)
# m_ngrams = af.load_ngrams(cleanedText, af.male_keywords, 3)
# print('m ngrams', m_ngrams)


matched_keywords = []
for sentence in listCleanSentences:
    for word in af.migrant_keywords:
        if word in sentence:
            matched_keywords.append(word)
print('There are', len(matched_keywords), 'keywords present from migrant keywords') # reads 9453

migrantesWords = []
for sentence in listCleanSentences:
    word = 'migrantes'
    if word in sentence:
        migrantesWords.append(word)
print('There are', len(migrantesWords), 'keywords present from migrant words') # reads 2287


# # get ngrams with one keyword first

migrantfirst = load_ngrams_onekeywordfirst(listCleanSentences, 'migrantes', 3)
migrantfirststop = load_ngrams_onekeywordfirst(token_sentences, 'migrantes', 3)

f_first = load_ngrams_onekeywordfirst(listCleanSentences, 'mujer', 3)
f_firststop = load_ngrams_onekeywordfirst(token_sentences, 'mujer', 3)

m_first = load_ngrams_onekeywordfirst(listCleanSentences, 'hombre', 3)
m_firststop = load_ngrams_onekeywordfirst(token_sentences, 'hombre', 3)

print('Migrant first:', migrantfirst)
print('Migrant first with stopwords:', migrantfirststop)
print('Female first:', f_first)
print('Female first with stopwords:', f_firststop)
print('Male first:', m_first)
print('Male first with stopwords:', m_firststop)


# get ngrams with all keywords first

migrantfirstall = load_ngrams_allkeywordsfirst(listCleanSentences, startswith_migrantkeywords, 3)
f_firstall = load_ngrams_allkeywordsfirst(listCleanSentences, startswith_female_keywords, 3)
m_firstall = load_ngrams_allkeywordsfirst(listCleanSentences, startwith_male_keywords, 3)

print('Migrant first all', migrantfirstall)
print('Female first all', f_firstall)
print('Male first all', m_firstall)


# save the ngrams to csv files

csvMigrantFirst = save_keywordfirst(migrantfirst, 'MigrantFirst.csv', 'keyword is migrant')
csvMigrantFirstStop = save_keywordfirst(migrantfirststop, 'MigrantFirstStop.csv', 'keyword is migrant')
csvMigrantFirstAll = save_keywordfirst(migrantfirstall, 'MigrantFirstAll.csv', 'keywords are migrant words')

csvFFirst = save_keywordfirst(f_first, 'F_First.csv', 'keyword is mujer')
csvFFirstStop = save_keywordfirst(f_firststop, 'F_FirstStop.csv', 'keyword is mujer')
csvFFirstAll = save_keywordfirst(f_firstall, 'F_FirstAll.csv', 'keywords are female words')

csvMFirst = save_keywordfirst(m_first, 'M_First.csv', 'keyword is hombre')
csvMFirstStop = save_keywordfirst(m_firststop, 'M_FirstStop.csv', 'keyword is hombre')
csvMFirstAll = save_keywordfirst(m_firstall, 'M_FirstAll.csv', 'keywords are male words')