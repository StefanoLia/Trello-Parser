# Trello-Parser
This repo contains a parser for Trello cards. It generates a **csv file** resuming all the meaningful information of each card.

## Detect hours
If you add in the description of a Trello cards the time you have spent to complete your task a new column will be generated in the resulting csv file.

### Format

Write in your card description the time in this format:

*|Time spent: **2h 20m**|*

No matters what text you write before the double dot, it parses the text after the ":" symbol. Characters "|" at the beginning and at the end are **necessary**.



## Start the program

1) Export your Trello board in a json file called *trello.json*

2) Put the file in the same directory of the script *parser.py*

3) Run the comand:

- python parser.py --all (take all the trello cards you have in your board)
- python parser.py (take all the cards in your "In progress" list. You must have it)

4) A file called "trello_activities.csv" will be generated at the end of the program