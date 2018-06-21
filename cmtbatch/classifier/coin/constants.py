from enum import Enum

"""
Used to identify feature extractors functions
"""
class FeatureExtractor(Enum):
    Unigram = "unigram",
    Bigram = "bigram"

"""
Used to split the dataset
"""
class InstanceType(Enum):
    Train = "train",
    Test = "test"