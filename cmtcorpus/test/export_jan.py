import contextlib
import csv
from datetime import datetime

import sys
from elasticsearch import Elasticsearch, helpers
from pytz import timezone
from dateutil.parser import parse
from twint.elasticsearch import RecycleObject

from clear_corpus2 import is_expected_activity, is_not_redundant


@contextlib.contextmanager
def nostdout():
    savestdout = sys.stdout
    sys.stdout = RecycleObject()
    yield
    sys.stdout = savestdout

def to_gmt_timezone(date_str):
    localtz = timezone('GMT')
    dt_unware = parse(date_str)
    dt_aware = localtz.localize(dt_unware)
    return dt_aware

with open("january.csv", encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter="|")

    it = 0
    for line in reader:
        if is_expected_activity(line) and is_not_redundant(line):
            it += 1
            print(it)
            date = line['date'] + ' ' + line['time']
            gmt_date = to_gmt_timezone(date)

            retweets_no = 0
            likes_no = 0
            replies_no = 0

            if line['retweets'] != '':
                retweets_no = int(line['retweets'])

            if line['likes'] != '':
                likes_no = int(line['likes'])

            if line['replies'] != '':
                replies_no = int(line['replies'])

            print(gmt_date)
            tweetObject = {
                "tweetid": line['id'],
                "created_at": gmt_date,
                "updated_at": datetime.now(),
                "timezone": line['timezone'],
                "text": line['tweet'],
                "hashtags": line['hashtags'],
                "username": line['username'],
                "retweets": retweets_no,
                "replies": replies_no,
                "likes": likes_no
            }

            j_data = {
                "_index": "analysis",
                "_type": "items",
                "_id": line['id'],
                "_source": tweetObject
            }

            actions = []
            actions.append(j_data)

            es = Elasticsearch('localhost:9200')

            with nostdout():
                helpers.bulk(es, actions, chunk_size=2000, request_timeout=200)
    import sys
    sys.exit("Finish")
