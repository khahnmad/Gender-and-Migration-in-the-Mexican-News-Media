# -*- coding: utf-8 -*-
"""
Created on Fri May 15 23:33:05 2020

@author: khahn
"""

# imports
import spacy
import pandas as pd
from nltk.tokenize import word_tokenize
import All_Functions as af
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
nlp = spacy.load('es_core_news_sm')

# Variables 
wordsThatArePeople = ['director','viceministro','alcalde','presidente',
                      'cineasta','cantante','expresidente','jefe','inspector',
                      'inmigrante','magnate', 'inspector','protagonista',
                      'productor','mentor','actor','autor','servidor','esposo',
                      'extranjero','juicio','agentes','sheriff','guardacostas',
                      'senador','joven','mexicano','trabajador', 'repartidor', 
                      'gobernador','constructor','poblano','profesor', 'solicitante',
                      'vecino', 'comisario','fiscal','juez','líder', 'africanos',
                      'subsecretario','etíopes','eritreos', 'nigerianos','hombre',
                      'dueño','extranjero', 'secretario','embajador',
                      'guatemalteco','conductor','funcionario', 'cabo',
                      'titular', 'canciller', 'criaturas','asesinato',
                      'representante','poblano','gobernador', 'secretario',
                      'panadero', 'manager','diputado','sacerdote', 'padre',
                      'empleador', 'pollero', 'hermano','portavoz','señora',
                      'migrante', 'guardia','vocero','periodista','migrantes', 
                      'extraficantes','vicepresidente','guatemalteca','alcaldesa',
                      'vicegobernadora', 'víctima','funcionaria', 'presidenta',
                      'esposa','autoridades','secretaria', 'doctor', 'viudo', 
                      'investigadora', 'mujer','procesadora', 'niña', 'jueza',
                      'policía','directora','actriz','mujeres','estudiantes',
                      'mexicanas','cameruneses','víctimas','esposas','personas',
                      'indocumentados','familias','latinos', 'héroes','lectores',
                      'obreros', 'sacerdotes', 'corruptos', 'varones', 'líderes',
                      'párroco', 'señores','egresados','transmigrantes',
                      'estudiantes', 'chavos','dueños', 'familiares','jóvenes', 
                      'diputados','niños','asaltantes','narcotraficantes', 
                      'pasajeros', 'hondureños','poblanos', 'conciudadanos','rusos',
                      'indígenas', 'pobres','legisladores','centroamericanos',
                      'americanos', 'hijos','infectados', 'asistentes','miembro',
                      'juzgados','habitantes','agricultores', 'productores',
                      'humanos', 'equipos','usuarios','especialistas','funcionarios',
                      'sobrevivientes','periodistas', 'hermanos','titulares',
                      'enfermos','granjeros', 'profesionales','vecindarios', 
                      'padres', 'mexicanos', 'franceses', 'jefes','congresistas',
                      'doctores','vecinos', 'familias','paisanos','avatares',
                      'miembros','investigadores', 'solicitantes', 'republicanos',
                      'indocumentados', 'demócratas', 'testigos', 'candidatos',
                      'activistas','refugiados', 'rohingyas', 'menores',
                      'trabajadores', 'propietarios','residentes','personas',
                      'personajes','centroamericano','hija', 'custodia' 'enfermera',
                      'caravana','persona','familiares','gente','mayordomos','robots',
                      'traficantes','pandillas','empresarios','extranjeros',
                      'presidentes', 'policías', 'pacientes', 'estadounidenses', 'ciudadanos',
                      'custodia', 'enfermera','caravanas', 'hordas','mentes',
                      'alicantino','príncipe', 'animador', 'arquitecto', 'rector',
                      'candidato', 'decenio', 'artista', 'portador', 'médico', 
                      'editor', 'poeta', 'reservista', 'bebé', 'pastor', 'papá', 
                      'chofer', 'investigador', 'especialista', 'expertos', 
                      'intérprete', 'austriaca', 'hombres', 'abuelita','paciente', 
                      'portadora', 'chicos','autora', 'neoyorquina','críticos',
                      'familia','sobrina','madre','doctora','abogada', 'gerente',
                      'pintora', 'camioneta','pilotos', 'profesora','académicos', 
                      'alumnos', 'integrantes', 'hombres', 'mujeres','seres', 
                      'reclusos', 'conmovedoras','músicos', 'encarcelados',
                      'jornaleros', 'inmigrantes', 'empleadores', 'portadores',
                      'polleros','viajeros', 'estereotipos', 'hispanos', 'latinoamericanos',
                      'editores',  'escritores', 'supervivientes', 'detenidos', 
                      'individuos','cocineros','médicos','coordinadores','guardacosta',
                      'delincuentes','huéspedes','ancianos', 'profesores', 'maestros',
                      'abusadores','científicas', 'ganadoras','niñas', 'enfermeras', 
                      'costureras','amigas', 'amiga', 'amigo', 'amigos','inmigrantes',
                      'encargadas','maestras','maestra', 'maestros', 'maestro',
                      'empleadas', 'maquiladoras','parejas','pareja', 'marido',
                      'maridos']
#clean this variable
peopleVocab = []
for item in wordsThatArePeople:
    if item not in peopleVocab:
        peopleVocab.append(item)

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
        while i < 5 and i + index < len(posdf):
            location = index + i
            if posdf[location] == 'NOUN': 
                searchedNoun = textdf[location]
                searchedNouns.append(searchedNoun)
                break 
            else:
                i += 1
    return searchedNouns
    
def get_token_sentences(sentence_list):
    return [word_tokenize(word) for word in sentence_list]

def sort_nouns(dataframe, article):
    peoplewords = []
#    notpeoplewords = []
    art_nouns = get_searchedNoun(article, dataframe)
#    for word in art_nouns:
#        if word not in notpeoplewords and word not in peopleVocab:
#            notpeoplewords.append(word)
    for word in art_nouns:
        if word in peopleVocab:
            peoplewords.append(word)
#    print(article, 'Not People Words:' ,notpeoplewords)
    return peoplewords


def load_possesiveNouns(pronoun, dataframe):
    indexes = []
    searchedWords = []
    pro_locations = getIndexes(dataframe, pronoun) # get the location of the article
    for elt in range(len(pro_locations)): # make a list of article indexes
        index = pro_locations[elt][0]
        indexes.append(index)
    textdf = dataframe['text']
    for index in indexes:
        location = index + 1
        if textdf[index] == pronoun:
            searchedWord = textdf[location]
            searchedWords.append(searchedWord)
    return searchedWords

def plot_frequency(text, title):
    counter = Counter(text)
    most = counter.most_common()
    x, y, = ([] for i in range(2))
    for word, count in most[:15]:
        x.append(word)
        y.append(count)
    sns.barplot(x=y, y=x, color='cyan').set_title(title)
    plt.show()
    

# open the articles
migrantCsvDirectory = 'C:/Users/khahn/PycharmProjects/HypothesisA/articleDB/migrants/migrants/' 
# get articles from migrant folder
urlsList = af.get_articles(migrantCsvDirectory)


# get text and format it
listsOfSentences = []
for url in urlsList:
    text = af.get_page_sentences(url) # gets stripped p tags from each url
    listsOfSentences.append(text)


one_list_sentences = []
for elt in listsOfSentences: # make it just one list of all the strings
    for i in elt:
        one_list_sentences.append(i)


next_text = ' '.join(one_list_sentences)
test_text = nlp(next_text)

df = pd.DataFrame()
df['text'] = [token.text for token in test_text]
df['part_of_speech'] = [token.pos_ for token in test_text]
  

el_nouns = sort_nouns(df, 'el')
la_nouns = sort_nouns(df, 'la')
los_nouns = sort_nouns(df, 'los')
las_nouns = sort_nouns(df, 'las')


print(len(el_nouns))
print(len(la_nouns))
print(len(los_nouns))
print(len(las_nouns))

el_nounsFreq = plot_frequency(el_nouns, 'El Nouns')
la_nounsFreq = plot_frequency(la_nouns, 'la_nouns')
los_nounsFreq = plot_frequency(los_nouns, 'los_nouns')
las_nounsFreq = plot_frequency(las_nouns, 'las_nouns')



#su_Freq = plot_frequency(su_nouns, 'Su_nouns')

testing_getindexes = getIndexes(df, 'su')
print('Got testing get indexes')
las_nouns = sort_nouns(df, 'su')
print('Got su sort nouns')
su_nouns = load_possesiveNouns(df, 'el')
