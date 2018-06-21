import cryptocompare
from datetime import datetime, timedelta

import pytz

from client.cryptocurrency.coin import CoinPropertyConstants as coin_property, Coin
from client.twitter.util import to_date, to_gmt


def get_coins():
    #xrp = Coin(1, "xrp", "Ripple", 1)
    #eth = Coin(2, "eth", "Ethereum", 2)
    #eos = Coin(3, "eos", "eos", 3)
    trx = Coin(3, "cmt", "CyberMiles", 3)
    coins = []
    coins.append(trx)
    #coins.append(eth)
    #coins.append(eos)
    return coins

def get_coin_price(coin_code, currency, time=None):
    return cryptocompare.get_historical_price(coin_code, currency, time)

def get_coin_list():
    coin_dict = cryptocompare.get_coin_list()

    coins = []
    for key, coin_data in coin_dict.items():
        id = int(coin_data[coin_property.ID])
        code = coin_data[coin_property.NAME]
        name = coin_data[coin_property.FULL_NAME]
        sortOrder = int(coin_data[coin_property.SORT_ORDER])
        coin = Coin(id, code.lower(), name.lower(), sortOrder)
        coins.append(coin)

    sorted_coins = sorted(coins, key=lambda x: x.sortOrder)
    return sorted_coins

if __name__ == "__main__":
    import time

    date_str = "2018-05-17T18:20:00.448083-07:00"
    date_gmt = to_date(to_gmt(date_str))
    timestamp = time.mktime(date_gmt.timetuple())
    print(timestamp)


    #price = get_coin_price("ZIL", "USD", date_gmt)
    #print(price['ZIL']['USD'])

