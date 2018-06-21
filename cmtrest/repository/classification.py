import pytz
from datetime import timedelta, datetime

from repository.util import to_date, to_local_timezone
from settings import get_mongo_client

client = get_mongo_client()
db = client['coinmarketrend']

def find_classification(coin_code, start_date, end_date):
    collection = db.get_collection(coin_code.lower())
    classifications = list(collection.find({}))
    #list(collection.find({'classification_date': {'$gte': start_date, '$lt': end_date}}))

    for classification in classifications:
        classification['_id'] = str(classification['_id'])
        classification['classification_date'] = to_date(to_local_timezone(classification['classification_date'])).isoformat()

    return classifications

if __name__ == "__main__":
    localtz = pytz.timezone('US/Pacific')
    from_str = "2018-05-02T00:00:00-07:00"
    _now = datetime.now(localtz).date()
    _from = to_date(from_str)
    classifications = find_classification("eos", _from.isoformat(), _now.isoformat())
    print(classifications)