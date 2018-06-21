from elasticsearch_dsl import Search
from classifier.influencer.influencer import calculate_user_score
from client.cryptocurrency.coin import Coin
from client.elastichsearch.constants import Influence
from settings import get_elasticsearch_client

es_client = get_elasticsearch_client()

def find_last_tweet(coin):
    filter = Search(using=es_client, index=coin.code.lower()).sort({"created_at" : {"order" : "desc"}})
    filter = filter[0:1]
    tweet = filter.execute()
    return tweet

def find_first_tweet(coin):
    filter = Search(using=es_client, index=coin.code.lower()).sort({"created_at" : {"order" : "asc"}})
    filter = filter[0:1]
    tweet = filter.execute()
    return tweet

def find_tweets(date_from, date_to, coin):
    filter = Search(using=es_client).filter('match', _index=coin.code.lower()).filter('range', created_at={'gte': date_from, 'lte': date_to})
    filter = filter[0:10000]
    tweets = filter.execute()
    return tweets

def find_user_influence_profile(username):
    filter = Search(using=es_client, index="influencer").filter('match', _id=username)
    profile = filter.execute()
    if len(profile) == 0:
        return None
    return profile

def find_max_actions():
    """
    :return: dictionary {"max_replies" : nr1, "max_likes" : nr2, "max_retweets" : nr3}
    """
    filter = Search(using=es_client, index="influencer").sort({"max_likes" : {"order" : "desc"}})
    likes = filter.execute()
    likes = likes[0]['max_likes']

    filter = Search(using=es_client, index="influencer").sort({"max_replies": {"order": "desc"}})
    replies = filter.execute()
    replies = replies[0]['max_replies']

    filter = Search(using=es_client, index="influencer").sort({"max_retweets": {"order": "desc"}})
    retweets = filter.execute()
    retweets = retweets[0]['max_retweets']

    return {Influence.MAX_LIKES : likes, Influence.MAX_REPLIES : replies, Influence.MAX_RETWEETS : retweets}

def find_user_score(username):
    max_dict = find_max_actions()
    usr_dict = find_user_influence_profile(username)
    return calculate_user_score(usr_dict[0], max_dict)

if __name__ == "__main__":
    eos = Coin(2, "eos", "eos", 2)
    print(find_last_tweet(eos))