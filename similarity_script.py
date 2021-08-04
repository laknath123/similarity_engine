# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 17:18:32 2021

@author: lakna
"""
# The are all the Packages that need to be loaded
import os
import gensim 
import sklearn
import random
import easygui

#import pdfplumber
#import csv

# nltk related libraries
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop = stopwords.words('english')
from tika import parser
from tika import unpack
import pandas as pd


from pathlib import Path
from sklearn.model_selection import train_test_split


def main():
    
    # The function that creates the menu
    def doc_simmilar_menu():
        choice = -1
        while choice not in (0,1,2,3,4):
            choice = int(input('''
    1. Building Permit
    2. Business Licence 
    3. Boards and Commission 
    4. Dog Licence
    0. If you have completed your selection Press 0
    What Type of Document are you planning to find a simillar document to: ''').strip())
            if choice not in (0,1,2,3,4):
                print("\nOption not valid! Please select a valid option (0-6).")
        return choice
    
    
    # This function calls the main doc_simillar function within and changes the directory based on the
    # the type of document you want to find    
    def directory_change ():   
        choice=doc_simmilar_menu()
        if choice == 1:
            os.chdir("C:\\Users\\lakna\\OneDrive\\Desktop\\CityGrows\\similarity_engine\\building_permits")  
        elif choice == 2:
            os.chdir("C:\\Users\\lakna\\OneDrive\\Desktop\\CityGrows\\similarity_engine\\business_licence")  
        elif choice == 3:
            os.chdir("C:\\Users\\lakna\\OneDrive\\Desktop\\CityGrows\\similarity_engine\\boards_and_comissions")  
        elif choice == 4:
            os.chdir("C:\\Users\\lakna\\OneDrive\\Desktop\\CityGrows\\similarity_engine\\dog_licence")  
    
    # This function leads to a easy gui window opening
    def obtain_file():
        filename = easygui.fileopenbox()
        return(filename)
    
    # This function calls the obtain_file and obtains the file path    
    def process_testfile():
        file = obtain_file()
        return(file)     
    
    
    # This function cleans specifically the test file 
    def test_clean(file):
        testdict=dict()    
        parsed=parser.from_file(file)
        line=parsed["content"]    
        tokens = nltk.word_tokenize(line)
        words_an=[word.lower() for word in tokens if word.isalpha()]
        words=[t for t in words_an if not t in stopwords.words("english")]
        testdict["test file"]=words
        
        return(testdict)
    
    
    
    # The function that creates the menu
    directory_change()
    
    #function that lets the user pick a file
    testfile=process_testfile()
    
    # This saves the cleaned test data into a dictionary
    testdata=test_clean(testfile)
    
    
    # Data Cleaning Function
    #read  each files in the directory, if you cant read it say you can't read and it continue 
    # The files that are printed are files that cannot be read
    
    
    
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
    
    # Once the training data and test_data is split, then add the new document to the test file
        
    def train_test(mytestdata):
        permitdict=cleaning()
        s = pd.Series(permitdict)
        training_data  = s.to_dict() 
        #adding the test data to the test list
        test_data=testdata # adding my test data to the test data dictionary
        # converting the each document that is stored in a list into a string.
        train_file =[]
        test_file = []
        for i in training_data.values():
            makeitastring = ' '.join(map(str, i))
            train_file.append(makeitastring)
        
        for i in test_data.values():
            makeitastring = ' '.join(map(str, i))
            test_file.append(makeitastring)
       # Storing the keys of the training and testing set to be used later 
        training_keys= list(training_data.keys())
        testing_keys = list(test_data.keys()) 
        
        return(train_file,test_file,training_keys,testing_keys)
    
    
    train_file,test_file,training_keys,testing_keys=train_test(testdata)
    
    #--------
    cleaning()
    train_test(testdata)
    
    # This is a function to add a tag to each of the documents
    #import smart_open
    
    def read_corpus(f, tokens_only=False):
            for i, line in enumerate(f):
                tokens = gensim.utils.simple_preprocess(line)
                if tokens_only:
                    yield tokens
                else:
                    # For training data, add tags
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
    
    #Function that adds tags
    def add_tags(trainfile,testfile):
        train_corpus = list(read_corpus(trainfile))                
        test_corpus = list(read_corpus(testfile, tokens_only=True))
        
        return(train_corpus,test_corpus)
    
    train_corpus,test_corpus=add_tags(train_file,test_file)
    
    
    def model(train_corpus,test_corpus):
        #Training Model
        model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
        # Building a vocabulary
        model.build_vocab(train_corpus)
        
        #Model test
        doc_id = random.randint(0, len(test_corpus) - 1)
        inferred_vector = model.infer_vector(test_corpus[doc_id])
        sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
        
        # Compare and print the most/median/least similar documents from the train corpus
        for label, index in [('MOST', 0)]:
            train_index =sims[index][0]
            print("Test Document is", testing_keys[doc_id])
            print("Most simillar train Document is", training_keys[train_index])
        
        
        #print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(test_corpus[doc_id])))
        print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
        for label, index in [('MOST', 0), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
            print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
    
    model(train_corpus,test_corpus)    
            



if __name__=='__main__':    
   main()
 
