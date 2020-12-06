### Get data from db ###

from pymongo import MongoClient

from os import environ 

def getDataFromDB(corpusSize):
    client = MongoClient(environ['MONGO_URI'])
    rss_item = client.rss.rss_item
    items = rss_item.find({ "stemmer": { "$exists": "true" }, "label": { "$exists": "true" }}, { "stemmer": 1, "label": 1, "_id": 0}).limit(corpusSize)
    data = []
    for item in items:
        data.append([item["stemmer"]["stemmed"], item["label"]])
    return data

""" TEST
for rssItem in getDataFromDB(1):
    print(rssItem)
    print()
"""

### Data pre-processing ###

from collections import defaultdict

from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def dataPreProcessing(data):
    data = " ".join(data.split())
    data = word_tokenize(data)
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    final_words = []
    word_Lemmatized = WordNetLemmatizer()
    for word, tag in pos_tag(data):
        if word not in stopwords.words('french') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
            final_words.append(word_Final)
    return final_words

""" TEST
test = "les tâches administratives, comme la gestion des factures ou le paiement des charges, et juridiques avec les déclarations urssaf et fiscales, par exemple.    #####  ##### communiquer avec les fédérations  la société autonomia portage dispense aussi des formations pour les métiers de coach, préparateur mental ou consultant, entre autres. actuellement plus de 280 personnes sont adossés à la société autonomia portage pour mener leur activité dans le secteur du sport, dont une trentaine d’athlètes. environ 75% d’entre elles continuent de travailler malgré la pandémie de covid-19, notamment grâce au télétravail. sébastien andré a relancé une campagne de communication auprès du ministère des sports et des fédérations pour faire connaître sa société et les avantages du statut de portage, « qu’ils fassent passer le message auprès des sportifs et des structures ».  –  plus d’information > https://www.portage-sport.fr/  –  ##### leslie mucret                      ###### articles similaires  ##### handball : adidas dévoile le nouveau maillot des équipes de france  déc 04, 2020  0  0  ##### handball : liqui moly partenaire titre de la starligue pour 5 ans  déc 03, 2020  0  0  ##### adidas lance le coloris « sunrise bliss » pour l’adizero adios pro  déc 01, 2020  1  0  ###### pas encore de commentaire...  ### publier un commentaire cancel reply  enregistrer mes données pour mes prochains commentaires.  oui, ajoutez moi à votre liste de diffusion.  ###### restez connectes  ###### le magazine du mois  formidable lien entre les pratiquants et ceux qui s’intéressent à leurs disciplines, sportmag ne se contente pas de traiter le sport comme la plupart des personnes le voient, le connaissent, l’appréhendent. sportmag va au-delà du sport…  mon compte sportmag club  cgv  mentions legales  contact  confidentialite  boutique  partenaires    site web by digital sport  © even’dia  2019 – tous droits réserves  "

print(dataPreProcessing(test))
"""

### Get or Create Corpus ###

from os import path

import pandas as pd 

def getOrCreateCorpus(corpusSize):
    if not path.exists("preProcessingData.csv"):
        all_data = getDataFromDB(corpusSize)
        for data in all_data:
            data[0] = dataPreProcessing(data[0])
        data_frame = pd.DataFrame(all_data, columns = ["text", "label"]) 
        data_frame.to_csv("preProcessingData.csv", index = False)
    return pd.read_csv("preProcessingData.csv")

""" TEST
corpus = getOrCreateCorpus()
print(corpus)
"""

### Training model ###

from sklearn import model_selection, naive_bayes, svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

corpus = getOrCreateCorpus(10000)

Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(corpus['text'], corpus['label'], test_size=0.3)

Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)

Tfidf_vect = TfidfVectorizer(max_features = 5000)
Tfidf_vect.fit(corpus['text'])

Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

SVM = svm.SVC(C = 1.0, kernel = 'linear', degree = 3, gamma = 'auto')
SVM.fit(Train_X_Tfidf, Train_Y)

predictions_SVM = SVM.predict(Test_X_Tfidf)
print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y) * 100)
