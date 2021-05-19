import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--json", default="results.json")
parser.add_argument("-q", "--query", required=True)
parser.parse_args()
print(parser.parse_args())

link = 'https://e-dostavka.by/'
response = requests.get(link).status_code

print(response)

