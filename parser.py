# modules
import os
import json
import pandas as pd
import time
from datetime import datetime
import re

# to fill
json_file = 'trello.json' # the json file to parse
end_dir = '' # the directory to store your cards

# open json
with open(json_file, encoding="utf8") as data_file:
    data = json.load(data_file)

# variables
cards = data["cards"]
card_number = 1
total_cards = len(data["cards"])
written_cards = 0

df = pd.DataFrame(columns=['Name', 'Member', 'Description', 'Time spent', 'Status', 'Due date'])

members = data["members"]
people_dict = {}

for member in members:
    people_dict[member["id"]] = str(member['fullName'])

boards = data['lists']
boards_names_dict = {}
for board in boards:
    boards_names_dict[board["id"]] = str(board["name"])

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

    # Time format: 2020-01-22T11:00:00.000Z
    df.loc[idx] = pd.Series({'Name': card['name'], 'Member': people_string, 'Description': desc, 'Time spent': time_spent, 
    'Status': boards_names_dict[card['idList']],
    'Due date': datetime.strptime(card['due'], "%Y-%m-%dT%H:%M:%S.%fZ") if card['due'] is not None else None})

print(df)
df.to_csv(end_dir+"trello_activities.csv", index=False, encoding='utf-8-sig')