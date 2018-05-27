
"""
Created on Sat Apr 21 13:55:06 2018

@author: Apurva
"""

from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.stem.porter import PorterStemmer
from nltk.tag.util import tuple2str
from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.parse.stanford import StanfordDependencyParser
#from nltk.parse.corenlp import CoreNLPDependencyParser


WN_TAG_LIST = {
    'NN': wn.NOUN,
    'VB': wn.VERB,
    'JJ': wn.ADJ,
    'RB': wn.ADV
    }

def deleteStopWords(wordList):
    stopWords=stopwords.words('english')
    return [word for word in wordList if word not in stopWords]

def get_semantic_features(tagged_tok, line):
    '''
    return features like synonyms, hypernyms, hyponyms, meronyms, holonymns
    extracted from each word of sentence
    '''
    lemma_sen = set()
    hyper_sen = set()
    hypo_sen = set()
    mero_sen = set()
    holo_sen = set()
    for word, tag in tagged_tok:
        if tag[:2] in WN_TAG_LIST:
            sense = lesk(line, word, pos=WN_TAG_LIST.get(tag[:2]))
            if not sense:
                continue
            for lem in sense.lemmas():
                lemma_sen.add(lem.name())
            for hyper in sense.hypernyms()[:30]:
                hyper_sen.add(hyper.name())
            for hypo in sense.hyponyms()[:30]:
                hypo_sen.add(hypo.name())
            for mero in sense.part_meronyms()[:30]:
                mero_sen.add(mero.name())
            for holo in sense.member_holonyms()[:30]:
                holo_sen.add(holo.name())
    return (' '.join(lemma_sen), ' '.join(hyper_sen), ' '.join(hypo_sen),
            ' '.join(mero_sen), ' '.join(holo_sen))

def get_lemmatized_line(tagged_tok):
    '''
    return lemmatized string
    '''
    wnl = WordNetLemmatizer()
    lemma_list = []
    for word, tag in tagged_tok:
        if tag[:2] in WN_TAG_LIST:
            word = wnl.lemmatize(word, pos=WN_TAG_LIST.get(tag[:2]))
        lemma_list.append(word)
    return ' '.join(lemma_list)

'''
def get_dependency_relations(line, q=False):
    
#    path_to_jar = 'stanford-corenlp-full-2018-02-27/stanford-corenlp-full-2018-02-27/stanford-corenlp-3.9.1.jar'
#    path_to_models_jar = 'stanford-corenlp-full-2018-02-27/stanford-corenlp-full-2018-02-27/stanford-corenlp-3.9.1-models.jar'
#    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    head_words = set()
    result = CONLDP.raw_parse(line)
    dep_tree = [r for r in result]
    dep_dict = dep_tree[0]
    root_word = dep_dict.root['word']
    for head, _, _ in dep_dict.triples():
        head_words.add(head[0])
    return ' '.join(head_words)

'''
def deeperNLPFeatures( dir_file = "./training/"):

    files = listdir(dir_file)
    stemmer = PorterStemmer()
    file_id = 0
    for f in files:
        file_id += 1 
        with open(dir_file + f, 'r', encoding = 'ISO-8859-1') as text_file:
            text = text_file.read()
            text = text.strip().lower()
            tokens = word_tokenize(text)
#            head_word = get_dependency_relations(text)
            tagged_tok = pos_tag(tokens)
            tagged_list = [tuple2str(t) for t in tagged_tok]
            tokens_clean = deleteStopWords(tokens)
            lemma_line = get_lemmatized_line(tagged_tok)
            stem_line = [stemmer.stem(t) for t in tokens_clean]
            synonyms, hypernyms, hyponyms, meronyms, holonymns = get_semantic_features(
                    tagged_tok, tokens)
            print(dir_file + f, ' ===> \n','text: \n',text, '\n','tokens: \n',tokens, '\n', 'pos tag: \n', tagged_tok, '\n', 'remove_stopWords: \n',tokens_clean, '\n', 'lemmatized: \n',lemma_line,'\n', 'stemmed: \n', stem_line, '\n', 'synonyms: \n',synonyms,'\n', 'hypernyms: \n', hypernyms,'\n', 'hyponyms: \n', hyponyms,'\n', 'meronyms: \n', meronyms, '\n', 'holonymns: \n',holonymns ,'\n\n' )

def main():
    print('Displaying feature set for each training faqs\n')
    print('***************************************************************************************************************')
    deeperNLPFeatures()
    print('***************************************************************************************************************')


if __name__ == '__main__':
    main()
