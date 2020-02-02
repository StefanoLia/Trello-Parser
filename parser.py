# modules
import os
import json
import pandas as pd
import time
from datetime import datetime
import re
import requests
import argparse


# initiate the argument parser
args_parser = argparse.ArgumentParser()
args_parser.add_argument("-all", "--all", help="take all the cards", action="store_true")

# read arguments from the command line
args = args_parser.parse_args()

with open('key.txt', "r") as f:
    key = f.readlines()[0]

with open('token.txt', 'r') as f:
    token = f.readlines()[0]

with open('id_board.txt', 'r') as f:
    id_board = f.readlines()[0]

# to fill
json_file = 'trello.json' # the json file to parse
end_dir = '' # the directory to store your cards

# open json
with open(json_file, encoding="utf8") as data_file:
    data = json.load(data_file)

url = 'https://api.trello.com/'
url_cards = url+'/1/boards/{}/cards?key={}&token={}'.format(id_board, key, token)
url_lists = url+'/1/boards/{}/lists?key={}&token={}'.format(id_board, key, token)
url_members = url+'/1/boards/{}/members?key={}&token={}'.format(id_board, key, token)

# variables
cards = requests.get(url_cards).json()
card_number = 1
total_cards = len(cards)
written_cards = 0

df = pd.DataFrame(columns=['Name', 'Member', 'Description', 'Time spent', 'Status', 'Due date'])

members = requests.get(url_members).json()
people_dict = {}

for member in members:
    people_dict[member["id"]] = str(member['fullName'])

lists = requests.get(url_lists).json()
lists_names_dict = {}
for l in lists:
    lists_names_dict[l["id"]] = str(l["name"])

# loop
for idx, card in enumerate(cards):
    print("Working on: " + card["name"])


    card_members = card['idMembers']
    people_string = ""
    for member_id in card_members:
        people_string += people_dict[member_id]+", "

    people_string = people_string[:-2]
    desc = card['desc']

    time_spent_match = re.search('\|\w+: ([^)]+)\|', desc)
    if time_spent_match is not None:
        string_to_remove = time_spent_match.group(0)
        time_spent = time_spent_match.group(1)

        desc = desc.replace(string_to_remove, '')
    else:
        time_spent = ""

    status = lists_names_dict[card['idList']]

    if args.all:
        # Time format: 2020-01-22T11:00:00.000Z
        df.loc[idx] = pd.Series({'Name': card['name'], 'Member': people_string, 'Description': desc, 'Time spent': time_spent, 
        'Status': status,
        'Due date': datetime.strptime(card['due'], "%Y-%m-%dT%H:%M:%S.%fZ") if card['due'] is not None else None})
    elif status == 'In progress':
        # Time format: 2020-01-22T11:00:00.000Z
        df.loc[idx] = pd.Series({'Name': card['name'], 'Member': people_string, 'Description': desc, 'Time spent': time_spent, 
        'Status': status,
        'Due date': datetime.strptime(card['due'], "%Y-%m-%dT%H:%M:%S.%fZ") if card['due'] is not None else None})

print(df)
df.to_csv(end_dir+"trello_activities_fastweb.csv", index=False, encoding='utf-8-sig')