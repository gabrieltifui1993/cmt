from repository.util import to_date, to_local_timezone
from settings import get_mongo_client

INFLUENCER_COLLECTION = "influencers"

client = get_mongo_client()
db = client['coinmarketrend']

def find_influencers(coin_code):
    collection = db[INFLUENCER_COLLECTION]
    influencers = list(collection.find({'coin_code': coin_code}).sort([("score", -1)]))
    unique_objects = list({object_['username']: object_ for object_ in influencers}.values())
    return unique_objects

if __name__ == "__main__":
    find_influencers("zil")
