from nltk.classify.util import apply_features
from collections import defaultdict

from classifier.coin.constants import InstanceType, FeatureExtractor
from classifier.coin.feature_extractor import unigram_word_feats, bigram_collocation_feats
from classifier.coin.util import split_data, find_all_words


class SentimentCalssifier:

    def __init__(self, dataset_dict, feature_extractors_dict, data_processor):
        """
        Constructor used to instantiate the classifier
        :param dataset_dict: dictionary containing the dataset e.g {"positive" : ["tweet1", "tweet2"], "negative" : ["tweet3"]}
        :param feature_extractors: dictionary containing functions
        """
        self.dataset_dict = dataset_dict
        self.feature_extractors_dict = feature_extractors_dict
        self.data_processor = data_processor
        self.feat_extractors = defaultdict(list)

    def train(self, train, test_ratio):
        """
            trains the chosen algorithm
        :param train: classification algorithm
        :param test_ratio: ratio of test documents from dataset
        :return:
        """
        dataset_dict = self.process(self.dataset_dict)

        # label each document with the coresponding class
        for class_label, documents in dataset_dict.items():
            dataset_dict[class_label] = [(document, class_label) for document in documents]

        #split dataset in test and training data. Get dict {"class_label" : [training_data], [test_data]"
        instances = defaultdict(list)
        for class_label, documents in dataset_dict.items():
            train_data, test_data = split_data(documents, test_ratio)
            instances[InstanceType.Train] = instances[InstanceType.Train] + train_data
            instances[InstanceType.Test] = instances[InstanceType.Test] + test_data

        tokenized_train_documents = [training_document for training_document in instances[InstanceType.Train]]

        training_words = [word for word in find_all_words(tokenized_train_documents)]

        unigram_feats = unigram_word_feats(training_words, top_n=2000)
        self.add_feat_extractor(self.feature_extractors_dict[FeatureExtractor.Unigram], unigrams=unigram_feats)

        #bigram_collocs_feats = bigram_collocation_feats([tokenized_train_tweet[0] for tokenized_train_tweet in tokenized_train_documents], top_n=1000, min_freq=5)
        #self.add_feat_extractor(self.feature_extractors_dict[FeatureExtractor.Bigram], bigrams=bigram_collocs_feats)

        training_set = apply_features(self.extract_features, tokenized_train_documents)
        self.classifier = train(training_set)

        labels_total = defaultdict(int)
        errors = defaultdict(int)
        for instance in instances[InstanceType.Test]:
            if len(instance[0]) > 1:
                classification = self.classify(instance[0])
                if classification != instance[1]:
                    errors[instance[1]] += 1
                labels_total[instance[1]] += 1

        acc_up = 0
        acc_down = 0

        for label, error in errors.items():
            total = labels_total[label]
            acc_up += total
            acc_down += total + error
            precision = ((total - error) / total) * 100
            print("{} class precision: {}".format(label, precision))

        accuracy = (acc_up / acc_down) * 100
        print("Accuracy: {}".format(accuracy))

    def classify(self, instance):
        instance_feats = apply_features(self.extract_features, [instance], labeled=False)
        return self.classifier.classify(instance_feats[0])

    def process(self, dataset_dict):
        """
            Processing the dictionary containing the dataset
        :return: processed documents
        """
        for class_label, documents in dataset_dict.items():
            dataset_dict[class_label] = self.data_processor.process_documents(documents)
        return dataset_dict

    #to be refactored
    def add_feat_extractor(self, function, **kwargs):
        self.feat_extractors[function].append(kwargs)

    #to be refactored
    def extract_features(self, document):
        all_features = {}
        for extractor in self.feat_extractors:
            for param_set in self.feat_extractors[extractor]:
                feats = extractor(document, **param_set)
            all_features.update(feats)
        return all_features