# modules
import os
import json
import pandas as pd

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

df = pd.DataFrame(columns=['Name', 'Member', 'Description', 'Complete', 'Due date'])

members = data["members"]
people_dict = {}

for member in members:
    people_dict[member["id"]] = str(member['fullName'])

# loop
for idx, card in enumerate(cards):
    print("Working on: " + card["name"])
    card_members = card['idMembers']
    people_string = ""
    for member_id in card_members:
        people_string += people_dict[member_id]+"\n"
    df.loc[idx] = pd.Series({'Name': card['name'], 'Member': people_string, 'Description': card['desc'], 'Complete': card['dueComplete'], 'Due date': card['dueComplete']})


print(df)
df.to_csv(end_dir+"trello_activities.csv")