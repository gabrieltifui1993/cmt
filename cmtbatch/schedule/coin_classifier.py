from cmath import log

import math

from client.elastichsearch.elastic_client import find_tweets, find_user_score
from client.twitter.util import to_local_timezone
from schedule.constants import Labels
from schedule.train_classifier import get_vote_classifier
from text_processing.data_processor import SocialTextProcessor


vote_classifier = get_vote_classifier(False)

def classify_tweets(_from, _to, coin):
    tweets = find_tweets(_from, _to, coin)
    pos = 0
    neg = 0

    #refactoring
    textpr = SocialTextProcessor

    good_tweets = 0
    for tweet in tweets:
        if "music" not in tweet.text and "award" not in tweet.text and tweet['username'] != "FoxNews":
            score = find_user_score(tweet['username'])
            pr_txt = textpr.process_document(tweet.text)
            if len(pr_txt) > 1:
                good_tweets+=1
                vote = vote_classifier.vote_classify(tweet.text)
                if vote == Labels.POS:
                    pos += 1 * (score + 0.5)
                else:
                    neg += 1 * (score + 0.5)
    print(good_tweets)
    if(good_tweets > 0):
        return math.log(pos + 0.5) - math.log(neg + 0.5), good_tweets
    else:
        return 0, 0