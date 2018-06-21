import csv
from datetime import datetime
import twint

client = twint.Config()

def build_file_name(_class, _from, _to):
    file_name_template = "{class_name}/blockchain/{_from}_{_to}.csv"
    file_name = file_name_template.format(class_name=_class,
                              _from = _from,
                              _to= _to)
    return file_name

def load_tweets(_class, _from, _to):
    client.Since = datetime.strftime(_from, '%Y-%M-%d')
    client.Until = datetime.strftime(_to, '%Y-%M-%d')
    client.Store_csv = True
    client.Search = "blockchain"
    client.Output = build_file_name(_class, client.Since, client.Until)
    twint.Search(client)

def scrapper_thread(periods_file, _class):
    with open(periods_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            date_from = datetime.strptime(row['FROM'], '%d-%M-%Y')
            date_to = datetime.strptime(row['TO'], '%d-%M-%Y')
            load_tweets(_class, date_from, date_to)

if __name__=="__main__":
    scrapper_thread('positive_periods1.csv', 'positive')
