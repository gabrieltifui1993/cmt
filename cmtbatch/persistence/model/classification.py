

class Classification_Type:
    SENTIMENT = "Sentiment"

class Classification(object):

    def __init__(self, coin_code, classification_type, classification_date, score, price_usd):
        self.coin_code = coin_code
        self.classification_type = classification_type
        self.classification_date = classification_date
        self.score = score
        self.price_usd = price_usd