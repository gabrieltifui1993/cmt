from nltk.corpus import stopwords as english_stopwords
from nltk.sentiment.util import mark_negation
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.wordnet import wordnet
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, TweetTokenizer, PunktSentenceTokenizer
import re
import string
from nltk.corpus import words as nltk_words

CONTRACTION_MAP = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

"""
class used as pattern for the oter text processing classes
"""
class AbstractDataProcessor:

    @classmethod
    def process_document(cls, document):
        """
            single document processor template
        :param document: to be processed document
        :return:
        """
        pass

    @classmethod
    def process_documents(cls, documents):
        """
            multiple documents processor
        :param documents: iterable collection
        :return: processed list of documents
        """
        processed_documents = []
        for document in documents:
            processed_documents.append(cls.process_document(document))
        return processed_documents

"""
    Social posts processor
"""
class SocialTextProcessor(AbstractDataProcessor):
    english_stopwords = english_stopwords.words()
    english_dictionary = dict.fromkeys(nltk_words.words(), None)
    my_stopwords = ["still", "just", "emoji", "new", "already"]
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    t_word_tokenizer = TweetTokenizer()
    sentence_tokenizer = PunktSentenceTokenizer()

    @classmethod
    def process_document(cls, document):

        document = cls.html_processing(document)

        #tokenize
        words = cls.t_word_tokenizer.tokenize(document)

        #expand contractions
        words = cls.expand_contractions(words)

        tagged_sentence = pos_tag(words)
        proper_nouns_tags = ['JJ', 'JJR', 'JJS', 'RB', 'RRB', 'RBS']
        tagged_sentence = [(word, tag) for word, tag in tagged_sentence if tag in proper_nouns_tags]

        words = []
        for word, tag in tagged_sentence:
            wordnet_tag = cls.find_wordnet_tag(tag)
            if wordnet_tag != '':
                word = cls.remove_apos(word)
                words.append(cls.lemmatizer.lemmatize(word, wordnet_tag))
            elif word in string.punctuation:
                words.append(word)

        #mark negation
        words = mark_negation(words)

        # must be reviewed
        stop_wrods = set(cls.english_stopwords + cls.my_stopwords)
        words = [word for word in words if word.lower() not in stop_wrods
                                        and word not in string.punctuation
                                        and len(word) > 1
                                        and cls.is_english_word(word.lower())
                                        ]

        # to lowercase
        words = list(map(str.lower, words))

        return words

    @classmethod
    def remove_apos(cls, text):
        while "'" in text:
            text = text.replace("'", "")
        return text

    @classmethod
    def expand_contractions(cls, words):
        expanded_words = []
        for word in words:
            if word.lower() in CONTRACTION_MAP.keys():
                expanded_words += word_tokenize(CONTRACTION_MAP[word.lower()])
            else:
                expanded_words.append(word)
        return expanded_words

    @classmethod
    def html_processing(cls, text):
        # remove urls
        text = re.sub(r"http\S+", ' ', text)

        # remove #
        text = re.sub(r'#(\S+)', r' \1 ', text)

        # remove digits
        text = re.sub(pattern=r"\d", repl=r"", string=text)

        # replace users, tags with empty space
        text = re.sub(r'@[\S]+', ' ', text)

        # Replace #word with empty space
        text = re.sub(r'#([^\s]+)', ' ', text)

        # remove duplicated characters
        text = re.sub(r'\s+', ' ', text)

        text = re.sub(r'(.)\1+', r'\1\1', text)

        return text

    @classmethod
    def find_wordnet_tag(cls, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''

    @classmethod
    def is_english_word(cls, word):
        try:
            cls.english_dictionary[word]
            return True
        except KeyError:
            return False

if __name__ == "__main__":
    text_processor = SocialTextProcessor
    while True:
        tweet = input("Insert tweet: ")
        processed_text = text_processor.process_document(tweet)
        print(processed_text)