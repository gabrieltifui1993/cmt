import os

from elasticsearch import Elasticsearch
from pymongo import MongoClient
from yaml import load

PROJECT_CONFIG = "config.yml"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE_PATH = os.path.join(PROJECT_ROOT, PROJECT_CONFIG)

with open(CONFIG_FILE_PATH, 'r') as ymlfile:
    classifier_config = load(ymlfile)


def get_mongo_client():
    url = classifier_config['mongo_url']
    port = classifier_config['mongo_port']
    return MongoClient(url, port)

def get_elasticsearch_client():
    url = classifier_config['elastic_url']
    return Elasticsearch(url)

if __name__ == "__main__":
    print(get_mongo_client())