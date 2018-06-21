

INFLUENCER_COLLECTION = "influencers"

class Influencer(object):

    def __init__(self, username, coin_code, score):
        self.username = username
        self.coin_code = coin_code
        self.score = score

    def __str__(self):
        return self.username + " " + str(self.score) + " " + self.coin_code