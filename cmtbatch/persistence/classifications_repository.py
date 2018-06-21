from client.twitter.util import to_date, to_local_timezone
from persistence.model.influence import INFLUENCER_COLLECTION
from persistence.model.word_cloud import WordCloud
from settings import get_mongo_client

client = get_mongo_client()
db = client['coinmarketrend']

def persist_influencer(influencer):
    collection = db[INFLUENCER_COLLECTION]
    collection.insert_one(influencer.__dict__)

def persist_word_cloud(word_cloud):
    collection = db[WordCloud.WORD_CLOUD_COLLECTION]
    collection.insert_one(word_cloud.__dict__)

def persist_classification(classification):
    collection = db[classification.coin_code.lower()]
    collection.insert_one(classification.__dict__)

def find_classification(coin_code, start_date, end_date):
    collection = db[coin_code.lower()]

    classifications = list(collection.find({'classification_date': {'$gte': start_date, '$lt': end_date}}))

    for classification in classifications:
        classification['_id'] = str(classification['_id'])
        classification['classification_date'] = to_date(to_local_timezone(classification['classification_date']))

    return classifications

