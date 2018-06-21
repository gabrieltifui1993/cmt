from enum import Enum
from yaml import load

class TwitterAuth(Enum):
    ConsumerKey = "consumer_key"
    ConsumerSecret = "consumer_secret"
    AccessToken = "access_token"
    AccessTokenSecret = "access_token_secret"
    ApiConfig = "api_config"


def get_twitter_api_config(config_file):
    """
        Get twitter api authentication config
    :return: dictionary containing necessary fields
    """
    with open(config_file, 'r') as ymlfile:
        twitter_config = load(ymlfile)

    return twitter_config[TwitterAuth.ApiConfig.value]