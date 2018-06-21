from collections import defaultdict
import os
from random import shuffle
import numpy
from nltk.classify import NaiveBayesClassifier
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.sentiment.util import (extract_unigram_feats, extract_bigram_feats)
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from classifier.coin.constants import FeatureExtractor
from classifier.coin.vote_classifier import VoteClassifier
from schedule.constants import Classifiers, Labels, CsvColumns
from settings import PROJECT_ROOT
from text_processing.data_processor import SocialTextProcessor
from yaml import load

CLASSIFIER_CONFIG_FILE = "classifier_config.yml"
CORPUS_PROPERTY = "corpus"
BUNDLE_PROPERTY = "bundle"
CLASS_PROPERTY = "class"
NAME_PROPERTY = "name"
DOCUMENTS_PROPERTY = "documents"

CLASSIFIER_CONFIG_FILE_PATH = os.path.join(PROJECT_ROOT, CLASSIFIER_CONFIG_FILE)

with open(CLASSIFIER_CONFIG_FILE_PATH, 'r') as ymlfile:
    classifier_config = load(ymlfile)

def get_vote_classifier(retrain=False):
    dataset = build_documents_dict()

    algs = {NaiveBayesClassifier : get_classifier_file(Classifiers.NAIVE_BAYES),
            SklearnClassifier(LinearSVC()): get_classifier_file(Classifiers.SVM),
            SklearnClassifier(MultinomialNB()): get_classifier_file(Classifiers.MULTINOMIAL_NB)
            }

    data_processor = SocialTextProcessor

    feature_extractor_dict = {FeatureExtractor.Unigram: extract_unigram_feats,
                              FeatureExtractor.Bigram: extract_bigram_feats}

    voteclassifier = VoteClassifier(algs, data_processor, feature_extractor_dict)
    voteclassifier.train(dataset, test_ratio=0.25, forced_retrain=retrain)



    return voteclassifier

def build_documents_dict():
    """
        builds documents dictionary
    :return: {"positive" : ['tweet1'], "negative" : ['tweet2']}
    """
    doc_paths = get_train_documents()

    docs_dict = defaultdict(list)
    for _class, paths in doc_paths.items():
        for path in paths:
            file_path = os.path.join(PROJECT_ROOT, path)
            if _class == Labels.MIXED:
                data = pd.read_csv(file_path, error_bad_lines=False)
                positive_tweets = data[data[CsvColumns.SENTIMENT] == Labels.POS][CsvColumns.TEXT].tolist()
                negative_tweets = data[data[CsvColumns.SENTIMENT] == Labels.NEG][CsvColumns.TEXT].tolist()
                docs_dict[Labels.POS] = docs_dict[Labels.POS] + positive_tweets
                docs_dict[Labels.NEG] = docs_dict[Labels.NEG] + negative_tweets
            else:
                data = pd.read_csv(file_path, error_bad_lines=False, delimiter="|")
                docs_dict[_class] = docs_dict[_class] + data[CsvColumns.TEXT].tolist()

    max_docs = numpy.minimum(len(docs_dict[Labels.POS]), len(docs_dict[Labels.NEG]))

    shuffle(docs_dict[Labels.POS])
    docs_dict[Labels.POS] = docs_dict[Labels.POS][:max_docs]

    shuffle(docs_dict[Labels.NEG])
    docs_dict[Labels.NEG] = docs_dict[Labels.NEG][:max_docs]

    return docs_dict

def get_train_documents():
    """
    documents for classifier training
    :return: dictionary {"class_name" : [full_path_document1, full_path_document2]}
    """
    classes_bundle = classifier_config[CORPUS_PROPERTY]

    docs_dict = defaultdict(list)
    for class_bundle in classes_bundle:
        _class = class_bundle[CLASS_PROPERTY]
        _class_name = _class[NAME_PROPERTY]
        docs_dict[_class_name] = _class[DOCUMENTS_PROPERTY]

    return docs_dict

def get_classifier_file(algorithm_name):
    """
    :param algorithm_name: the algorithm name of the classifier to be loaded
    :return: pickle file
    """
    classifiers = classifier_config["classifiers"]
    for classifier in classifiers:
        algorithm = classifier['algorithm']
        if algorithm['name'] == algorithm_name:
            return "file://"+os.path.join(PROJECT_ROOT, algorithm['file'])

#test
if __name__ == "__main__":
    get_vote_classifier(True)