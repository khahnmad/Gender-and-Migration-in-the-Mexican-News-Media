import requests
import time
import httplib2
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

# goal:get headline of web page
# inputs: url
# return: headline
def get_page_headline (url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    headline = soup.find('h1').get_text().strip()
    return headline

# goal: get page sentences
# inputs: url
# return: list of sentences
def get_page_sentences(url):
    stripped_sentences, final_sentences = ([] for i in range(2))
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    list_paragraphs = soup.find_all('p')
    stripped_sentences = [tag.get_text().strip() for tag in list_paragraphs]
    norm_esp = Cucco()
    norms = ['replace_punctuation', 'remove_extra_whitespaces']
    for sentence in stripped_sentences:
        if len(sentence) > 0:
            final_sentences.append(norm_esp.normalize(sentence, norms))
    return final_sentences

# goal: get tokenized sentences
# inputs: sentence_list
# return: list of token sentences (list of list)
def get_token_sentences(sentence_list):
    return [word_tokenize(word) for word in sentence_list]

# goal: create corpus of sentences to analyze
# inputs:
# return: list of sentences
def create_corpus_by_url(url_list):
    corpus = []
    for url in url_list:
        headline = get_page_headline(url)
        sentence_list = get_page_sentences(url)
        for sentence in sentence_list:
            corpus.append(sentence)
    return corpus

# goal: create dataframe (df) for analysis
# inputs: urls_list,
# return: d
def create_dataframe(urls_list):
    df_urls, df_newspaper, df_headlines, df_sentences_list, df_dates = ([] for i in range (5))
    # collect data for each article
    for url in urls_list:
        df_urls.append(url)
        df_newspaper.append('nothing')
        df_headlines.append(get_page_headline(url))
        df_sentences_list.append(get_page_sentences(url))
        df_dates.append('nothing')

    # intialise data of lists
    data = {
        'url': df_urls,
        'newspaper': df_newspaper,
        'headline': df_headlines,
        'sentences_list': df_sentences_list,
        'date': df_dates
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    df.to_csv(r'export_data.csv', index=False, encoding='utf-8-sig')
    return df

# goal: search for related words in specific (keyword) sentences
# inputs: sentence_list, keyword_list
# return:  list of related words
def search_related_words (sentence_list, keyword_list):
    token_sentences, matched_sentences, related_words_list = ([] for i in range(3))
    new_stopwords = set(stopwords.words('spanish')) - {'ella', 'ellas', 'una', 'unas', 'él'}
    quotations = ['“', '”', 'así', 'hace', 'Por']
    new_stopwords.update(quotations)

    # token sentences
    token_sentences = get_token_sentences(sentence_list)

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

# goal: todo: search for keywords
# inputs: sentence_list, keyword_list
# return:  list of related words
def search_keywords(sentence_list, keyword_list):
    return 0
# goal: show the frequency
# inputs:
# return:
def show_word_frequency (word_list, title):
    counter = Counter(word_list)
    most = counter.most_common()
    x, y = [], []
    for word, count in most[:15]:
        x.append(word)
        y.append(count)
    sns.barplot(x=y, y=x, color='cyan').set_title(title)
    plt.show()


# goal: todo: generate urls selenium by keywords_topic
# inputs: keyword_topic
# return: map list (keyword, url)
def generate_urls_google ():
    # import parameters / dataframes
    # df_newspaper_param = pd.read_csv('parameters - newspapers_list.csv')
    # df_keywords_list = [] pd.read_csv('')
    # df = pd.read_excel(r'Path where the Excel file is stored\File name.xlsx', sheet_name='your Excel sheet name')

    # inputs
    # newspapers_urls_list = df_newspaper_param['url']
    # female_keywords_list = df_newspaper_param['female']
    keywords_list = ['Mexico mujer', 'mujer inmigrante']
    newspapers_urls_list = ['https://sintesis.com.mx', 'https://heraldodepuebla.com']

    #outputs
    urls_list = []

    # actions:
    driver = webdriver.Chrome()
    driver.get('http://www.google.com/')
    for keyword in keywords_list:
        for newspaper_url in newspapers_urls_list:
            element_searched = 'site:'+newspaper_url+' '+keyword+' after:2017'
            search_box = driver.find_element_by_name('q')
            search_box.clear()
            search_box.send_keys(element_searched)
            search_box.submit()
            print(element_searched)

            #GET LINKS
            # soup = BeautifulSoup(requests.get(driver.current_url).text, "lxml")
            # http = httplib2.Http()
            # status, response = http.request(driver.current_url)
            # for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
            #     if link.has_attr('href') and newspaper_url in link:
            #         urls_list.append(link.get('href'))
            # items = driver.find_elements_by_tag_name('a')
            # items_text = items.text
            # print(items_text)
            # for item in items:
            #     link = item.get_attribute('href')
            #     print(link)
            #     if newspaper_url in link:
            #         urls_list.append(link)
    print(urls_list)
    driver.quit()
    return urls_list

# goal: todo: get_parameters_list
# inputs: keyword_list
# return: url_list
def get_parameters_list (parameter_name):
    return 0