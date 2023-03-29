# ClimbingBot
A bot you can use if you are into climbing/bouldering to keep track of your topped routes.

# How to use?

## 1. Option A: Create a file called .env and paste the following:

```
telegram-api-key=YOUR TELEGRAM API KEY
telegram-chat-id=ID OF THE CHAT

database-path=data/database.sqlite
```

## 1. Option B: Rename the .env.example file to .env and change its values.


After doing so, insert your telegram API key and the ID of the chat, where the bot should be running.

## 2. Now open up a terminal and run following commands:

```
cd C:\path\to\this\folder\
python run.py
```

# What commands can I use?
At the moment, following commands are supported:

| Command | Action |
|---|---|
| /start | Starts a session and displays the grade keyboard. |
| /end | Ends a session and removes the grade keyboard again. |
| /ranking | Displays a ranking for all users of this bot. |
| /chart | Displays a chart with data of the topped routes. |
| /chart [username] | 'Displays a chart with data of the topped routes for the given user. |
| /session | Displays your statistics of the current session. |
| /session [username] | Displays the statistics of the given user of the current session. |
| /stats | Displays your all time statistics |
| /stats [username] | Displays the all time statistics of the given user. |
| /help | Displays the help section. |
