from client.twitter.util import to_date


class Tweet(object):

    def __init__(self, params_dict):
        self.twitter_id = params_dict.get("id")
        self.text = params_dict.get("text")
        self.sentiment = None
        self.sentiment_score = None
        self.created_at = to_date(params_dict.get("created_at"))
        self.author = Author(params_dict.get("user"))

    def __repr__(self):
        return str(self.created_at) + self.text

    def __str__(self):
        return str(self.created_at) + self.text

class Author(object):

    def __init__(self, params_dict):
        self.twitter_id = params_dict.get("id")
        self.name = params_dict.get("name")
        self.followers_count = params_dict.get("followers_count")
        self.friends_count = params_dict.get("friends_count")
        self.favourites_count = params_dict.get("favourites_count")
        self.created_at = to_date(params_dict.get("created_at"))
        self.verified = params_dict.get("verified")
        self.location = params_dict.get("location")
        self.url = params_dict.get("url")
        self.retweet_rate = None
        self.like_rate = None
        self.reply_rate = None