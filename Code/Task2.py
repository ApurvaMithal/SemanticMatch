# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 15:30:18 2018

@author: Apurva
"""

import os
import collections
import re
import sys
import operator

training_set = dict()
test_question = dict()

def getData(dataSet):
    directory = "./training/"
    for dir_entry in os.listdir(directory):
        dir_entry_path = os.path.join(directory, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as text_file:
                text = text_file.read()
                text = text.strip().lower()
                dataSet.update({dir_entry_path: Faq(text, bagOfWords(text))})


def bagOfWords(text):
    bagsofwords = collections.Counter(re.findall(r'\w+', text))
    return dict(bagsofwords)


class Faq:
    text = ""
    word_freqs = {}


    def __init__(self, text, counter):
        self.text = text
        self.word_freqs = counter

    def getText(self):
        return self.text

    def getWordFreqs(self):
        return self.word_freqs

   
def main():
    
    text = input('Enter user input: faq to be matched   ')
    text = text.strip().lower()
    shared_items = dict()
    
    test_question.update({'user input': Faq(text, bagOfWords(text))})
    for key,value in test_question.items():
        user_keys = set(value.word_freqs)
    
    getData(training_set)
    print("======================================================Training data===================================================================")
    for key_train,value_train in training_set.items():
        print (key_train , " => " , "\n", value_train.text, "\n\n", value_train.word_freqs, "\n\n")
            
    print("======================================================Testing data===================================================================")
    for key,value in test_question.items():
        print (key , " => " , "\n", value.text, "\n\n", value.word_freqs, "\n\n")
        
        
    for key_train,value_train in training_set.items():
        train_keys = set(value_train.word_freqs)
        common_items = set(train_keys) & set(user_keys)
        shared_items.update({key_train: len(common_items)})
        print('key_train:  ',key_train, '   common_items: ' ,common_items, '  ', len(common_items))

    sorted_dict = dict(sorted(shared_items.items(), key=operator.itemgetter(1), reverse=True))
    sorted_dict_top = dict(sorted(shared_items.items(), key=operator.itemgetter(1), reverse=True)[:10])
    
    print("===================Sorted Training FAQ and commom words frequency count with user FAQ ================================================")
    for key,value in sorted_dict.items():
        print (key , " => " , value)
    
    print("\n===================Top 10 Sorted Training FAQ and commom words frequency count with user FAQ =========================================\n")
    for key,value in sorted_dict_top.items():
        print (key,' ===> ', training_set[key].text, "\n\n")
        print('<*******************>')
            
            
if __name__ == '__main__':
    main()
    