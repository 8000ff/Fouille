---
geometry: margin=1.5cm
---

# Rendu sp1

Projet commun :
 - Clément Malléjac
 - Thomas Brochot

## Diagramme UML du projet

### Architecture du projet

Un diagramme de composant fut nécessaire afin de modéliser l'architecture hétérogène de ce projet.

![diagramme de composant](SP1/doc/diag_comp.png)

Deux parties se distinguent dans cette architecture.

1) Le backend

Elle a pour objectif d'aspirer et de stocker le plus de données possible d'internet. Pour cela, un daemon s'occupe d'orchestrer trois principaux types d'agents.
  - Collecteurs : A partir des flux RSS fournis, ils aspirent toutes les données possibles des articles et les stockent dans la base MongoDB.
  - Décorateurs : Une fois les données brutes disponibles, ils s'occupent de les nettoyer.
  - Exporteur : Alimenter la base Elastic avec les données nettoyées.

2) Le frontend

Il s'agit de la partie auquel l'utilisateur aura directement à faire. Elle contient :
 - Une interface web
 - Une base de données ElasticSearch

### Structure des données

Aucune structure précise des données n'a été établie. Une base orientée document est donc tout à fait pertinente.

Cependant, les deux bases ont chacune un objectif :
 - MongoDB : Stocker toutes les données brutes récupérables des items RSS, tel que les pages html, des images ou encore des hyperliens, données de classification, etc...
 - ElasticSearch : Stocker les données nettoyées et pertinentes reçues par l'Exporter. Elles seront destinées à la recherche.

## Ressources nécessaires à l'éxécution

L'application nécessite :
 - Python (PSF)
 - MongoDB (GNU AGPL pour les outils, Apache 2.0 pour les pilotes)
 - NodeJS (Licence X11)

## Test utilisable

### 0. Installer les dépendances

Dans le dossier SP1

```bash
pip3 install pymongo BeautifulSoup feedparser
npm install browserContentCollector/
```

### 1. Démarrer une base MongoDB

Exemple en local :

```bash
mkdir test_db
mongod --dbpath=test_db
```

### 2. Ajouter l'URI de la base MongoDB à l'environnement

Exemple avec la base locale :

```bash
export MONGO_URI=mongodb://localhost:27017
```

### 3. Lancer le test

La commande suivante :
- Ajoute les url des flux RSS à la base MongoDB
- Attaque les flux et créee des documents rss/rss_item dans la base MongoDB
- Pour chaque document rss/rss_item, attaque la page web de l'item RSS, récupère le contenu html et l'ajoute au document
- Pour chaque document rss/rss_item, nettoie le contenu html précédemment acquis et le stocke dans une nouvelle variable de l'item_rss
- Pour chaque document rss/rss_item, exporte les champs préalablement définis dans exporter/exporter.py vers la base ElasticSearch

```bash
make add_feed test_rss test_content test_content_cleaner test_exporter
```

Par défaut le test ne traitera que 10 items RSS, utilisez la variable n pour changer ce comportement (ne pas oublier la regle **clean** qui va supprimer les fichier temporaires)

```bash
make clean add_feed test_rss test_content n=100
```


## Codes externes utilisés

### python :

BeautifulSoup :
 - Licence : MIT
 - Description : Beautiful Soup est une bibliothèque qui permet de récupérer facilement des informations sur des pages Web

pymongo : 
 - Licence : Apache Software License (Apache License, Version 2.0)
 - Description : La distribution PyMongo contient des outils pour interagir avec la base de données MongoDB à partir de Python

asyncio : 
 - Licence : PSF (GPL compatible)
 - Description : Le module asyncio fournit une infrastructure pour écrire du code simultané à thread unique à l'aide de coroutines, multiplexer l'accès aux E / S sur des sockets et d'autres ressources, exécuter des clients et des serveurs réseau et d'autres primitives associées

feedparser :
 - Licence : BSD License (BSD-2-Clause)
 - Description : Analyser les flux Atom et RSS en Python

### Javascript :

puppeteer :
 - Licence : Apache-2.0
 - Description : Puppeteer est une bibliothèque de Node qui fournit une API de haut niveau pour contrôler Chrome ou Chromium via le protocole DevTools

mongodb : 
 - Licence : Apache-2.0
 - Description : Le pilote officiel MongoDB pour Node.js. Fournit une API de haut niveau au-dessus de mongodb-core qui est destinée aux utilisateurs finaux

shuffle-array :
  - Licence : MIT
  - Description : Randomisez l'ordre des éléments dans un tableau donné à l'aide de l'algorithme de Fisher-Yates 