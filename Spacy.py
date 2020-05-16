# -*- coding: utf-8 -*-
"""
Created on Fri May 15 23:33:05 2020

@author: khahn
"""

# imports
import spacy
import pandas as pd


# Functions 
# gets toples with the positions of a value in a dataframe
# input: pd dataframe, value to find
def getIndexes(dataframe, value):
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dataframe.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

# gets the noun that follows a given article 
# input: article to search for, dataframe with colums 'part_of_speech' and 'text'
def get_searchedNoun(article, dataframe):
    indexes = []
    searchedNouns = []
    art_locations = getIndexes(dataframe, article) # get the location of the article
    for elt in range(len(art_locations)): # make a list of article indexes
        index = art_locations[elt][0]
        indexes.append(index)
    posdf = dataframe['part_of_speech']
    textdf = dataframe['text']
    for index in indexes:
        i = 1        
        while i < 5:
            location = index + i
            if posdf[location] == 'NOUN':
                searchedNoun = textdf[location]
                searchedNouns.append(searchedNoun)
                break 
            else:
                i += 1
    return searchedNouns
    

text1 = 'El gobernardo de Coahuila, Miguel Riquelme Solís, y el fiscal general Gerardo Márquex, confirmaron la detención de dos personas por el triple feminicidio de las trabajadoras del IMSS, ocurrido este jueves por la noche'
text2 = 'En la actual gestión presidencial se han registrado 20 días sin homicidios a escala nacional'
text = [text1, text2]

nlp = spacy.load('es_core_news_sm')
test_text = nlp(text1)

df = pd.DataFrame()
df['text'] = [token.text for token in test_text]
df['part_of_speech'] = [token.pos_ for token in test_text]


# runs the function 
el_nouns = get_searchedNoun('el', df)
print(el_nouns)
la_nouns = get_searchedNoun('la', df)
print(la_nouns)
