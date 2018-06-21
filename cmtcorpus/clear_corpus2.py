import csv
import glob

import os

from nltk import FreqDist
from pymongo import MongoClient
from textblob import TextBlob

from constants import HAPPY_EMOJI, SAD_EMOJI
from data_processor import SocialTextProcessor

min_retweets = 5
min_replies = 5
min_likes = 0


pol =  0.1
subj = 0.1

class WordCloud(object):

    WORD_CLOUD_COLLECTION = "word_cloud"

    def __init__(self, coin_code, words):
        self.coin_code = coin_code
        self.words = words

fieldnames = [
			"id",
			"date",
			"time",
			"timezone",
			"user_id",
			"username",
			"tweet",
			"replies",
			"retweets",
			"likes",
			"location",
			"hashtags",
			"link"
		]

def persist_tweet(tweet, output):
    if not (os.path.exists(output)):
        with open(output, "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="|")
            writer.writeheader()

    with open(output, "a", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="|")
        writer.writerow(tweet)

def is_expected_activity(data):
    try:
        return int(data['retweets']) > min_retweets or \
               int(data['likes']) > min_replies or \
               int(data['replies']) > min_likes
    except Exception as e:
        return False

def is_expected_sentiment(data):
    analysis = TextBlob(data['tweet'])
    return analysis.sentiment.polarity > pol and analysis.sentiment.subjectivity > subj

def get_words(data):
    text_pr = SocialTextProcessor
    result = text_pr.process_document(data['tweet'])
    return result

def contains_emoji(data, emoji_map):
    return any(emoji in data['tweet'] for emoji in emoji_map)


def persist_word_cloud(word_cloud):
    url = 'localhost'
    port = 27017
    client = MongoClient(url, port)
    db = client['coinmarketrend']
    collection = db['word_cloud']
    collection.insert_one(word_cloud.__dict__)

def build_word_cloud(documents_path):
    all_words = []

    i = 0
    for filename in glob.glob(documents_path):
        print(filename)
        with open(filename, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")
            for tweet in reader:
                words = get_words(tweet)
                if is_expected_activity(tweet) and len(words) > 1 or contains_emoji(tweet, SAD_EMOJI):
                    i += 1
                    print(i)
                    print(words)
                    all_words = all_words + words

    allWordDist = FreqDist(word.lower() for word in all_words)
    word_cloud = WordCloud('wcng', allWordDist.most_common(1000000))
    print(allWordDist.most_common(1000000))
    persist_word_cloud(word_cloud)

if __name__ == "__main__":
    #clear_retweets()
    file = "wc_neg/*.csv"
    build_word_cloud(file)
