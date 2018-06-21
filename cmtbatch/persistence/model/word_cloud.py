
class WordCloud(object):

    WORD_CLOUD_COLLECTION = "word_cloud"

    def __init__(self, coin_code, words_date, words):
        self.coin_code = coin_code
        self.words_date = words_date
        self.words = words
