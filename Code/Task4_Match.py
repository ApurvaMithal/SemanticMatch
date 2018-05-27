# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 14:09:25 2018

@author: Apurva
"""

'''
faq matching using NLP features
'''

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.tag.util import tuple2str
from nltk.stem import PorterStemmer

from Task4_Index import get_semantic_features
from Task4_Index import get_lemmatized_line
from Task4_Index import deleteStopWords
#from indexer import get_dependency_relations

import pysolr

def match(query, method, instance_url):
    '''
    search solr index using user query
    '''
    q_list = []
    q_string = ''
    solr = pysolr.Solr(instance_url)
    
    tokens = word_tokenize(query)
    stemmer = PorterStemmer()
    tagged_tokens = pos_tag(tokens)
    tagged_list = [tuple2str(t) for t in tagged_tokens]
    tokens_clean = deleteStopWords(tokens)
    lemmas = get_lemmatized_line(tagged_tokens)
    stem_line = [stemmer.stem(t) for t in tokens_clean]
    synonyms, hypernyms, hyponyms, meronyms, holonyms = get_semantic_features(
        tagged_tokens, tokens)
#        head_words = get_dependency_relations(lemmas, True)
    print('user input features', ' ===> \n','text: \n',query, '\n','tokens: \n',tokens, '\n', 'pos tag: \n', tagged_tokens, '\n', 'remove_stopWords: \n',tokens_clean, '\n', 'lemmatized: \n',lemmas,'\n', 'stemmed: \n', stem_line, '\n', 'synonyms: \n',synonyms,'\n', 'hypernyms: \n', hypernyms,'\n', 'hyponyms: \n', hyponyms,'\n', 'meronyms: \n', meronyms, '\n', 'holonymns: \n',holonyms ,'\n\n' )

    pos_tag_data = '&'.join(tagged_list)
    lemmas = '&'.join(lemmas.split())
    stems = '&'.join(stem_line)
    synonyms = '&'.join(synonyms.split())
    hypernyms = '&'.join(hypernyms.split())
    hyponyms = '&'.join(hyponyms.split())
    holonyms = '&'.join(holonyms.split())
    meronyms = '&'.join(meronyms.split())
    
    if method == 3:
#        head_words = '&'.join(head_words.split())
        if tokens:
            q_list.append('text:' + '&'.join(tokens))
        if tokens_clean:
            q_list.append('text_clean:' + '&'.join(tokens_clean))
        if pos_tag_data:
            q_list.append('pos_tag:' + pos_tag_data)
        if lemmas:
            q_list.append('lemmas:' + lemmas)
        if stems:
            q_list.append('stems:' + stems)
        if synonyms:
            q_list.append('synonyms:' + synonyms)
        if hypernyms:
            q_list.append('hypernyms:' + hypernyms)
        if hyponyms:
            q_list.append('hyponyms:' + hyponyms)
        if meronyms:
            q_list.append('meronyms:' + meronyms)
        if holonyms:
            q_list.append('holonymns:' + holonyms)
#            if head_words:
#                q_list.append('head_word:' + head_words)
    if method == 4:
        if tokens:
            q_list.append('text:' + '&'.join(tokens) + '^0.5')
        if pos_tag_data:
            q_list.append('pos_tag:' + pos_tag_data + '^0.02')
        if lemmas:
            q_list.append('lemmas:' + lemmas + '^4')
        if tokens_clean:
            q_list.append('text_clean:' + '&'.join(tokens_clean) + '^5')
        if stems:
                q_list.append('stems:' + stems + '^1.5')
        if synonyms:
            q_list.append('synonyms:' + synonyms + '5')
        if hypernyms:
            q_list.append('hypernyms:' + hypernyms + '^5')
#       if hyponyms:
#                 q_list.append('hyponyms:' + hyponyms + '^4')
#         if head_words:
#                q_list.append('head_word:' + head_words + '^0.5')
#         if meronyms:
#                 q_list.append('meronyms:' + meronyms + '^1.4')
#         if holonyms:
#                 q_list.append('holonymns:' + holonyms + '^1.4')
                
    q_string = ', '.join(q_list)
    print('The Solr query is q=%s, fl=\'id,text\'\n' % (q_string))
    result = solr.search(q=q_string, fl='id,text')
    for r in result:
        print(r['id'])
        print(' '.join(r['text']))
def main():
    '''
    main function
    '''
    instance = 'http://localhost:8983/solr/collection_1/'

    print('Performing improved deep NLP pipeline faq matching...')
    line = input('Enter match query: ')
    line = line.strip().lower()
    match(line, 3, instance)
    print('\n*********************************************************************************************\n')
    print('\n\nPerforming improved deep NLP pipeline faq matching with heuristics such that higher weight is given to more important features like hypernyms, synonyms \n' )
    match(line, 4, instance)
    print('\n*********************************************************************************************\n')

if __name__ == '__main__':
    main()
    