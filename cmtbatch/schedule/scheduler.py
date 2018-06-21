from datetime import datetime, timedelta
import pytz
import twint
from nltk import FreqDist
from dateutil.parser import parse
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread

from client.cryptocurrency.coin import Coin
from client.cryptocurrency.cryptocompare_client import get_coins, get_coin_price
from client.elastichsearch.elastic_client import find_last_tweet, find_tweets, find_user_score, find_first_tweet
from client.elastichsearch.tweet_loader import load_tweets
from client.twitter.util import to_date, to_gmt
from persistence.classifications_repository import persist_classification, persist_word_cloud, find_classification, \
    persist_influencer
from persistence.model.classification import Classification, Classification_Type
from persistence.model.influence import Influencer
from persistence.model.word_cloud import WordCloud
from schedule.coin_classifier import classify_tweets
from text_processing.data_processor import SocialTextProcessor

scheduler = BlockingScheduler()

def get_scheduler():
    return scheduler

#@scheduler.scheduled_job('interval', minutes=1)
def classify_sched():
    coins = get_coins()
    for coin in coins:
        classify_thread = Thread(target=classify_job, args=(coin,))
        classify_thread.start()

def classify_job(coin):
    fromdate = parse(find_first_tweet(coin)[0]['created_at'])
    todate = parse(find_last_tweet(coin)[0]['created_at']) + timedelta(hours=2)
    print(fromdate, todate)
    hours = (todate - fromdate).total_seconds() / 3600
    for i in range(0, int(hours), 4):
        from_range = fromdate + timedelta(hours=i)
        to_range = fromdate + timedelta(hours=i+1)
        classify_new_tweets(coin, from_range.isoformat(), to_range.isoformat(), from_range.isoformat())

    build_word_cloud(coin, fromdate, todate)
    build_influencers(coin)

def load_and_classify_job(coin):
    localtz = pytz.timezone('US/Pacific')

    todate = datetime.now(localtz)

    try:
        last_tweet = find_last_tweet(coin)
        from_date = last_tweet[0]['created_at']
        print(from_date)
    except Exception:
        from_date = (datetime.now(localtz) + timedelta(days=-30)).isoformat()

    print("Loading tweets from {} to {}".format(from_date, (todate+ timedelta(days=1)).isoformat()))
    load_tweets(from_date, (todate+ timedelta(days=1)).isoformat(), coin)

    #recover
    hours = (todate - parse(from_date)).total_seconds() / 3600
    for i in range(0, int(hours)):
        from_range = to_date(from_date) + timedelta(hours=i)
        to_range = to_date(from_date) + timedelta(hours=i+1)
        classify_new_tweets(coin, from_range.isoformat(), to_range.isoformat(), from_range.isoformat())

    #last classification
    todate_new = datetime.now(localtz)
    fromdate_new = datetime.now(localtz) - timedelta(hours=-1)
    classify_new_tweets(coin, fromdate_new.isoformat(), todate_new.isoformat(), fromdate_new.isoformat())
    build_influencers(coin)

def classify_new_tweets(coin, fromdate, todate, classification_date):
    print(classification_date)
    score = classify_tweets(fromdate, todate, coin)
    classification = Classification(coin.code, Classification_Type.SENTIMENT, classification_date, score[0], 0)
    persist_classification(classification)
    build_word_cloud(coin, fromdate, todate)


def build_word_cloud(coin, from_date, to_date):
    print("iso",from_date)
    tweets = find_tweets(from_date, to_date, coin)

    textpr = SocialTextProcessor
    cleared_tweets = [textpr.process_document(tweet.text) for tweet in tweets]

    all_words = []

    for tweet in cleared_tweets:
        all_words = all_words + tweet

    allWordDist = FreqDist(word.lower() for word in all_words)

    word_cloud = WordCloud(coin.code, from_date, allWordDist.most_common(100))
    persist_word_cloud(word_cloud)

def build_influencers(coin):
    from_date = datetime.now() - timedelta(hours=720)
    to_date = datetime.now()
    tweets = find_tweets(from_date.isoformat(), to_date.isoformat(), coin)

    for tweet in tweets:
        username = tweet['username']
        score = find_user_score(username)
        influencer = Influencer(username, coin.code, score)
        print(influencer)
        persist_influencer(influencer)

if __name__ == "__main__":
    classify_sched()
    #localtz = pytz.timezone('US/Pacific')

    #fromdate = datetime.now(localtz) + timedelta(days=-30)
    #todate = datetime.now(localtz)
    #crypto = Coin(3, "crypto", "crypto", 3)
    #load_tweets(fromdate.isoformat(), todate.isoformat(), crypto)