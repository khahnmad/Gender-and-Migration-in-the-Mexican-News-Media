# Imports
import All_Functions as af
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# open the articles
migrantCsvDirectory = 'C:/Users/khahn/PycharmProjects/HypothesisA/articleDB/migrants/migrants/' # get articles from migrant folder
urlsList = af.get_articles(migrantCsvDirectory)


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

male_related_words = af.search_related_words(one_list_sentences, 'Male Keywords')
female_related_words = af.search_related_words(one_list_sentences, 'Female Keywords')

m_text = ' '.join(male_related_words)
wordcloud = WordCloud().generate(m_text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

f_text = ' '.join(female_related_words)
wordcloud = WordCloud().generate(f_text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
