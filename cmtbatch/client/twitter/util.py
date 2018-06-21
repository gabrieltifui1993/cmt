import arrow
from dateutil.parser import parse
from datetime import datetime
from pytz import timezone


def build_hashtag_query(coin):
    return "#{} OR #{}".format(coin.code, coin.name)

def build_words_query(coin):
    return "{} OR {}".format(coin.code, coin.name)

def build_keywords_list(coin):
    return [coin.code, coin.name, "#"+coin.code, "#"+coin.name]

def to_date(date_str):
    return parse(date_str)

def to_local_timezone(date_str):
    return arrow.get(parse(date_str)).to('local').format()

def to_gmt(date_str):
    return arrow.get(parse(date_str)).to('GMT').format()

def to_utc_timezone(date_str):
    localtz = timezone('US/Pacific')
    dt_unware = datetime.strptime(date_str, '%I:%M %p - %d %b %Y')
    dt_aware = localtz.localize(dt_unware)
    return dt_aware

def to_utc_aware(dt_unware):
    localtz = timezone('US/Pacific')
    dt_aware = localtz.localize(dt_unware)
    return dt_aware

def is_valid(tweet):
    try:
        tweet["retweeted_status"]
        is_retweet = True
    except KeyError:
        is_retweet = False

    return not is_retweet

#10:26 AM - 24 Apr 2018 2018-04-24 10:26:00+00:00

if __name__ == "__main__":
    pacific = to_utc_timezone("10:54 AM - 24 Apr 2018")
    print(pacific)
    print(arrow.get(pacific).to('local').format())