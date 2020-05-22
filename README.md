# Gender and Migration in the Mexican News Media

This code is part of an ongoing project analyzing the representation of immigrant women in the Mexican news media, particulary the news media in Puebla. 


I have three hypotheses: 

- The news talks about female immigrants less than their actual representation in migratory flows. 
- Female immigrants are characterized as paassive, gendered, racialized victims, despite their diverse and dynamic roles. 
- These characterizations are more or less nuanced depending on the origins of the women, her location, and the stage in the migratory process. 

## Results for "Count Gender Frequency" (As of 5/6/20)
[link to code](https://github.com/khahnmad/Gender-and-Migration-in-the-Mexican-News-Media/blob/master/Count%20Gender%20Frequency.py)

*PACKAGES USED:* 
csv, nltk, collections, glob, os, seaborn, matplotlib

*INPUT:*

1) Import the functions necessary from the [All_Functions](https://github.com/khahnmad/Gender-and-Migration-in-the-Mexican-News-Media/blob/master/All_Functions.py) file

2) Import 85 urls from 4 csv files. The urls were collected by searching the words 'migrante', 'migrantes', 'inmigrantes', and 'inmigrante' in the Mexican newspapers Sintesis, Sexenio,	Publimetro,	Diaro Cambio, and	El Universal, and taking the top 5 results for each search. 

*OUTPUT:*

1) A count of how many times female-gendered and male-gendered words appear in the articles

2) A [barplot](https://github.com/khahnmad/Gender-and-Migration-in-the-Mexican-News-Media/blob/master/MostCommonKeywords.png) of the most frequent gendered keywords and how often they appeared in the articles

## Mock Results for "Wordcloud"
*PACKAGES USED:*
matplotlib, wordcloud

This code makes wordclouds based on the words that frequently appear in sentences with male-gendered words and female-gendered words given a corpus of articles about migration in Mexico.

## Mock Results for "Spacy"
*PACKAGES USED:*
pandas, spacy

This code is experimenting with Spacy. Given an article in text, it finds the noun that corresponds with the article. 


## Mock Results for "Keyword Searching"

*PACKAGES USED:* 

requests, BeautifulSoup, nltk.corpus, nltk.tokenize, cucco, seaborn, collections, matplotlib.pyplot


*INPUT:* 

1) Urls from news articles

2) Indicate whether searching sentences for immigrant-related keywords or gender-related keywords


*OUTPUT:*

Two barplots that indicate the most frequent words that appeared in the same sentence as the keywords. 

See [Migrant Keywords Chart](https://github.com/khahnmad/Gender-and-Migration-in-the-Mexican-News-Media/blob/master/Migrant%20Keywords%20Chart.png) and [Gendered Keywords Chart](https://github.com/khahnmad/Gender-and-Migration-in-the-Mexican-News-Media/blob/master/Gendered%20Keywords%20Chart.png) for these barplots. 



## Mock Results for "Hypothesis A"

*PACKAGES USED:*  

numpy, requests, BeautifulSoup, Cucco, nltk.corpus, nltk, nltk.tokenize, urllib.request

*OUTPUT:*

The 20 most common words from the three articles fed into the program in the beginning

migrantes: 5 derechos: 3 Destacó: 2 organización: 2 Por: 2 ejemplo: 2 Puebla: 2 medalla: 2 defensor: 2 aseveró: 2 una: 2 mundo: 2 haga: 2 labor: 1 director: 1 Saber: 1 Es: 1 Poder: 1 favor: 1 ser: 1



