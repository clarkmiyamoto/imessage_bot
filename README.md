# imessage_bot
Currently stuck in quarentine and am very bored. On my list of morally-gray things to do, I've always wanted to create a chatbot which immitates me for when I'm socially drained.

This bot trains on previous iMessage data. 

## Installaiton 
You need to install...
- `chatterbot`

## Setup
1. Go into `System Preferences` -> `Security` -> `Full Disk Access` and give `Terminal` permissions.
2. Go to `/Users/{your username}/Library/Messages/chat.db` and copy that file into the `imessage_bot` folder. I have .gitignore set to ignore all .db files so you don't have to worry about your personal info getting uploaded to GitHub.

# How to use
Turn on chatbot for specific person.
1. Go into `Training Chat Bot.ipynb`, find index associated with target phone number
2. Start the bot:
```
python main.py <phone_number>
```
Format of phone_number: "+18081231234"

# Improvements
- Find way to clean data
- Use better trainer (probably from `transformers` or `NLTK`)