# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 11:59:37 2021

@author: lakna
"""
#Required Library's
import os
import gensim 
import sklearn
import random


import pdfplumber
import csv

# nltk related libraries
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop = stopwords.words('english')
from tika import parser
from tika import unpack
import pandas as pd

import json

def cleaning():
        permitdict=dict()
        for permit in os.listdir():
            parsed = parser.from_file(permit)
            line=parsed["content"]
            try:
                tokens = nltk.word_tokenize(line)
                words_an=[word.lower() for word in tokens if word.isalpha()]
                words=[t for t in words_an if not t in stopwords.words("english")]
                permitdict[permit]=words
            except TypeError:
                print("The following PDF could not be parsed\n",permit)        
        return(permitdict)        
   


root="C:/Users/lakna/OneDrive/Desktop/CityGrows/similarity_engine/"
boardsdir=root+"boards_and_comissions"
os.chdir(boardsdir)


boardsdata=cleaning()
unclean_data=pd.DataFrame.from_dict(boardsdata, orient='index')
unclean_data.to_csv("C:/Users/lakna/OneDrive/Desktop/CityGrows/similarity_engine/raw_datafields/boardsdata.csv")


buildingdir=root+"building_permits"
os.chdir(buildingdir)
buildingdata=cleaning()

unclean_data=pd.DataFrame.from_dict(buildingdata, orient='index')
unclean_data.to_csv("C:/Users/lakna/OneDrive/Desktop/CityGrows/similarity_engine/raw_datafields/buildingdata.csv")

bizlicence = root+"business_licence"
os.chdir(bizlicence)
bizdata=cleaning()
unclean_data=pd.DataFrame.from_dict(bizdata, orient='index')
unclean_data.to_csv("C:/Users/lakna/OneDrive/Desktop/CityGrows/similarity_engine/raw_datafields/bizdata.csv")

doglicence = root+"dog_licence"
os.chdir(doglicence)
dogdata=cleaning()
unclean_data=pd.DataFrame.from_dict(dogdata, orient='index')
unclean_data.to_csv("C:/Users/lakna/OneDrive/Desktop/CityGrows/similarity_engine/raw_datafields/dogdata.csv")
