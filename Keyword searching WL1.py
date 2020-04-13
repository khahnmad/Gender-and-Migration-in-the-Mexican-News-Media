# Imports
import textAnalysis as ta

# Parameters/ Variables
keywords1 = ['inmigrante', 'migrante', 'migración', 'inmigrantes', 'migrantes', 'migratoria']
keywords2 = ['hombre', 'padre', 'niño','niños', 'esposo', 'hombres', 'padres', 'esposos', 'masculina', 'masculino']
keywords3= ['mujer', 'niñas', 'niña', 'madre', 'mujeres', 'esposa', 'esposas', 'madres', 'femenino', 'femenina']
keywords4 = ['género', 'adolescente', 'adulta']

migrantes_url_list = [
    # 'https://www.capitalmexico.com.mx/cdmx/crisis-en-derechos-humanos-acarrea-retos-nuevos-a-la-antropologia-social-especialistas/',
    # 'https://www.capitalmexico.com.mx/estados/se-compromete-sre-a-tomar-medidas-con-los-migrantes-varados-en-la-frontera-para-evitar-brotes-de-covid-19/',
    # 'https://www.capitalmexico.com.mx/nacional/pandemia-por-covid-19-es-un-reto-mayor-segob/',
    # 'https://www.capitalmexico.com.mx/estados/tabasco/mnpt-pide-al-inm-medidas-precautorias-luego-del-motin-registrado-en-tenosique-tabasco/',
    # 'https://www.capitalmexico.com.mx/nacional/cndh-solicita-a-inm-y-comar-implementas-medidas-cautelares-para-personas-en-estaciones-migratorias/',
    # 'https://sintesis.com.mx/puebla/2020/01/07/nelly-maceda-pide-castigo-a-funcionarios-que-propicien-la-trata-de-personas-o-el-trafico-ilegal-de-migrantes/',
    # 'http://www.diariopuntual.com/internacional/2018/07/18/1843',
    # 'https://sintesis.com.mx/puebla/2020/03/26/vences-valencia-pide-proteccion-para-migrantes-ante-pandemia/',
    'https://sintesis.com.mx/puebla/2020/03/21/armando-prida-huerta-entrega-la-medalla-gilberto/',
    'https://sintesis.com.mx/puebla/2019/12/18/pasaportes-menores-retorno-migrantes/',
    'https://sintesis.com.mx/puebla/2019/07/07/inmigrantes-viaje-averno/',
    'https://www.elpopular.mx/2018/11/08/mundo/mexico-tiene-mas-migrantes-de-eu-que-de-centroamerica-193207']

# generate urls list from google
url_list = ta.generate_urls_google()
# based on the urls, create a corpus of token sentences (list of list)
corpus = ta.create_corpus_by_url(migrantes_url_list)
print("Corpus: ")
print(corpus)
print("Fin Corpus")

# search for sentences matching keywords
migrant_related_words = ta.search_keyword_related_words(corpus, keywords1)
# male_related_words = ta.search_keyword_related_words(corpus, keywords2)
# female_related_words = ta.search_keyword_related_words(corpus, keywords3)

# show frequecy plot for keywords1
ta.show_word_frequency(migrant_related_words, 'Migrant Keyword - Related Words')
# ta.show_word_frequency(male_related_words, 'Gendered Keywords - male Related words')
# ta.show_word_frequency(female_related_words, 'Gendered Keywords - fem Related words')