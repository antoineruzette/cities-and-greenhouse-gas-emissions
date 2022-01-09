#!/usr/bin/env python
# coding: utf-8

# -----------------------------------------------------------
# City-wide emissions project, unstructured data part.
# This file contains a class with functions to process 
# natural language, using textblob.
# -----------------------------------------------------------

from textblob import TextBlob
from nltk.corpus import stopwords

class Text_Processor:
    
    def __init__(self, content, collection_words):
        self.content = content
        self.blob = TextBlob(self.content)
        self.collection_words = collection_words
        
    def __str__(self):
        return f"{self.content}"

    def lemmatize_with_postag(self):
        """Lemmatize the object, using the appropriate pos tags."""
        tag_dict = {"J": 'a', 
                "N": 'n', 
                "V": 'v', 
                "R": 'r'}
        words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in self.blob.tags] 
        lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
        self.content = " ".join(lemmatized_list)
        self.blob = TextBlob(self.content)

    def clean_collection_words(self, collection_words):
        """Clean the string by removing collection words, specified in collection_words."""
        clean_string = [word for word in self.blob.words if word not in 
                        collection_words]
        self.content = " ".join(clean_string)
        self.blob = TextBlob(self.content)
    
    def clean_stopwords(self):
        """Clean the string by removing stop words of the english language."""
        self.clean_collection_words(stopwords.words('english'))
    
    def process(self, lemmatize, clean_collection_words, clean_stopwords):
        """Processes the string according to the arguments: first argument indicates whether lemmatization needs to be performed, selcond argument indicates whether collection words need to be removed, third argument indicates whether stopwords need to be removed."""
        if(lemmatize == True):
            self.lemmatize_with_postag()
        if(clean_collection_words == True):
            self.clean_collection_words(self.collection_words)
        if(clean_stopwords == True):
            self.clean_stopwords()
        return self.content