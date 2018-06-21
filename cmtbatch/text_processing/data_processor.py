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
from text_processing.constants import CONTRACTION_MAP

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
    my_stopwords = ["still", "just", "emoji", "open", "go", "coin", "see"]
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    t_word_tokenizer = TweetTokenizer()
    sentence_tokenizer = PunktSentenceTokenizer()

    @classmethod
    def process_document(cls, document):

        document = cls.html_processing(document)

        #tokenize
        words = cls.t_word_tokenizer.tokenize(document)

        #print(" \n Tokenizing: {} \n".format(words))
        #expand contractions
        words = cls.expand_contractions(words)
        #print("Expanding contractions: {} \n".format(words))

        # to lowercase
        words = list(map(str.lower, words))

        tagged_sentence = pos_tag(words)
        proper_nouns_tags = ['IN', 'NNP', 'PRP', 'PRP$', 'WP$']
        tagged_sentence = [(word, tag) for word, tag in tagged_sentence if tag not in proper_nouns_tags]

        #print("Filtering tags: {} \n".format(tagged_sentence))

        words = []
        for word, tag in tagged_sentence:
            wordnet_tag = cls.find_wordnet_tag(tag)
            if wordnet_tag != '':
                word = cls.remove_apos(word)
                words.append(cls.lemmatizer.lemmatize(word.lower(), wordnet_tag))
            elif word in string.punctuation:
                words.append(word)

        #print("Lemmatize: {} \n".format(words))
        # must be reviewed
        words = [word for word in words if word not in string.punctuation
                                        and len(word) > 1
                                        and cls.is_english_word(word.lower())
                                        ]
        #print("Punctuation and english: {} \n".format(words))

        words = mark_negation(words)
        #print("Negation: {} \n".format(words))

        stop_wrods = set(cls.english_stopwords + cls.my_stopwords)
        words = [word for word in words if word.lower() not in stop_wrods]

        #print("Stop words: {} \n".format(words))


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
        tweet = input("Tweet: ")
        processed_text = text_processor.process_document(tweet)
