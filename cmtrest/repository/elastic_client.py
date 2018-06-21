from elasticsearch_dsl import Search
from settings import get_elasticsearch_client

es_client = get_elasticsearch_client()

TWEET_URL = "https://twitter.com/nouser/status/"


class Tweet(object):

    def __init__(self, id, text, username):
        self.id = id
        self.text = text
        self.username = username
        self.url = TWEET_URL + str(id)

def find_last_important_tweets(coin_code):
    filter = Search(using=es_client, index=coin_code).sort({"retweets" : {"order" : "desc"}}
                                                           ,{"replies" : {"order" : "desc"}}
                                                           ,{"likes" : {"order" : "desc"}}
                                                           )
    tweets_data = list(filter.execute())

    tweets = []
    for tweet_data in tweets_data:
        tweet = Tweet(id = tweet_data['tweetid'], text = tweet_data['text'], username=tweet_data['username'])
        tweets.append(tweet)

    return tweets

if __name__ == "__main__":
    tweets = find_last_important_tweets("zil")
    for tweet in tweets:
        print(tweet.text)