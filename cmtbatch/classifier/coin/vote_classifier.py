from nltk.data import load
from statistics import mode

from classifier.coin.sentiment_classifier import SentimentCalssifier
from classifier.coin.util import save_classifier


class VoteClassifier:

    def __init__(self, classification_algorithms, data_processor, feature_extractor_dict):
        """
        :param classifiers: dictionary of classifier algorithms {algorithm : file.pickle}
        """
        self.classification_algorithms = classification_algorithms
        self.trained_algorithms = {}
        self.data_processor = data_processor
        self.feature_extractor_dict = feature_extractor_dict

    def train(self, dataset, test_ratio, forced_retrain = False):
        for algorithm, file in self.classification_algorithms.items():
            dataset_copy = dict(dataset)
            if forced_retrain:
                self.train_algorithm(algorithm, file, dataset_copy, test_ratio)
            else:
                try:
                    self.trained_algorithms[algorithm] = load(file)
                except LookupError:
                    self.train_algorithm(algorithm, file, dataset_copy, test_ratio)

    def train_algorithm(self, algorithm, file, dataset, test_ratio):
        sentiment_classifier = SentimentCalssifier(dataset, self.feature_extractor_dict, self.data_processor)
        sentiment_classifier.train(algorithm.train, test_ratio=test_ratio)
        self.trained_algorithms[algorithm] = sentiment_classifier
        classifier_save_path = file.replace('file://', '')
        save_classifier(sentiment_classifier, classifier_save_path)

    def vote_classify(self, instance):
        votes = []
        for algorithm, trained_classifier in self.trained_algorithms.items():
            processed_tweet = self.data_processor.process_document(instance)
            vote = trained_classifier.classify(processed_tweet)
            votes.append(vote)

        return mode(votes)