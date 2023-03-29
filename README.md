# ClimbingBot
A bot you can use if you are into climbing/bouldering to keep track of your topped routes.

# How to use?
To run the bot, you have to create a file called .env and insert following content:

```
telegram-api-key=YOUR TELEGRAM API KEY
telegram-chat-id=ID OF THE CHAT

database-path=data/database.sqlite
```

Insert you telegram API key and the ID of the chat, where the bot should be running.

After you have done this, open up a terminal and run following commands:

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
| /session | Displays your statistics of the current session. |
| /session [username] | Displays the statistics of the given user of the current session. |
| /stats | Displays your all time statistics |
| /stats [username] | Displays the all time statistics of the given user. |
| /help | Displays the help section. |
