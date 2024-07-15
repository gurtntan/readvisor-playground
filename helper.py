import os
import csv
import json

openai_api_key = os.environ['openai_api_key']


def csv_to_json(csv_filepath, json_filepath):
    with open(csv_filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    with open(json_filepath, 'w') as file:
        json.dump(data, file, indent=4)

csv_to_json('data/reviews.csv', 'data/reviews.json')



