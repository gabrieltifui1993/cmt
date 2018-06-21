import csv
import glob

import os

from textblob import TextBlob

from constants import HAPPY_EMOJI, SAD_EMOJI
from data_processor import SocialTextProcessor

fieldnames = [
			"label",
			"total",
		]

def persist(row, output):
    if not (os.path.exists(output)):
        with open(output, "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="|")
            writer.writeheader()

    with open(output, "a", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="|")
        writer.writerow(row)

def calculate_totals(documents_path, output_document, _class):
    total = 0
    for filename in glob.glob(documents_path):
        with open(filename, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")
            total += len(list(reader))

    dict = {
        "label": _class,
        "total": total,
    }
    persist(dict, output_document)

if __name__ == "__main__":
    output = "analysis/totals.csv"

    file = "negative/*.csv"
    #calculate_totals(file, output, "negative")

    file = "positive/*.csv"
    #calculate_totals(file, output, "positive")

    output = "analysis/cleared_totals.csv"

    file = "cleared/no_retweets/positive.csv"
    calculate_totals(file, output, "cleared positive")

    file = "cleared/no_retweets/negative.csv"
    calculate_totals(file, output, "cleared negative")
