from settings import get_mongo_client

client = get_mongo_client()
db = client['coinmarketrend']

def find_word_cloud(coin_code):
    collection = db[WordCloud.WORD_CLOUD_COLLECTION]
    word_clouds = list(collection.find({'coin_code': coin_code}).sort([("_id", -1)]).limit(1))
    return word_clouds

class WordCloud(object):

    WORD_CLOUD_COLLECTION = "word_cloud"

    def __init__(self, coin_code, words_date, words):
        self.coin_code = coin_code
        self.words_date = words_date
        self.words = words

if __name__ == "__main__":
    coin_code = "ocn"
    find_word_cloud(coin_code)