import codecs
import pickle

from sklearn.model_selection import train_test_split

def split_data(dataset, training_ratio):
    train, test = train_test_split(dataset, test_size = training_ratio, shuffle=False)
    return train, test

#to be rewrited
def find_all_words(documents, labeled=None):
    all_words = []
    if labeled is None:
        labeled = documents and isinstance(documents[0], tuple)
    if labeled == True:
        for words, sentiment in documents:
            all_words.extend(words)
    elif labeled == False:
        for words in documents:
            all_words.extend(words)
    return all_words

def save_classifier(content, filename):
    """
    Store `content` in `filename`. Can be used to store a SentimentAnalyzer.
    """
    print("Saving", filename)
    with codecs.open(filename, 'wb') as storage_file:
        # The protocol=2 parameter is for python2 compatibility
        pickle.dump(content, storage_file, protocol=2)