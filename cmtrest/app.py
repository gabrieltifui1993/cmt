from flask import Flask
from flask_cors import CORS
import json

from repository.classification import find_classification
from repository.elastic_client import find_last_important_tweets
from repository.influence import find_influencers
from repository.wordcloud import find_word_cloud

app = Flask(__name__)
cors = CORS(app)

@app.route('/api/sentiment/<string:coin_code>/<string:start_date>/<string:end_date>', methods=['GET'])
def get_sentiment(coin_code, start_date, end_date):
    print(coin_code, start_date, end_date)
    classifications = find_classification(coin_code, start_date, end_date)
    print(classifications)
    return json.dumps([ob for ob in classifications])

@app.route('/api/tweets/<string:coin_code>', methods = ['GET'])
def get_last_important_tweets(coin_code):
    tweets = find_last_important_tweets(coin_code)
    return json.dumps([ob.__dict__ for ob in tweets])

@app.route('/api/influencer/<string:coin_code>', methods=['GET'])
def get_influencers(coin_code):
    influencers_coll = find_influencers(coin_code)

    influencers = []
    for influencer in influencers_coll:
        influencer.pop('_id')
        influencers.append(influencer)

    return json.dumps(influencers)

@app.route('/api/wordcloud/<string:coin_code>', methods=['GET'])
def get_wordcloud(coin_code):
    word_cloud = find_word_cloud(coin_code)
    return json.dumps(build_d3wordcloud(word_cloud[0]['words']))

def build_d3wordcloud(words):
    d3_data = []
    for word in words:
        d3_instance = {
            'text' : word[0],
            'size' : word[1]
        }
        d3_data.append(d3_instance)
    return d3_data

if __name__ == '__main__':
    app.run(port='5002')