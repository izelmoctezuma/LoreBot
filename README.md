# Lore Checker Bot

The Lore Checker Bot is a Discord bot designed to make character-heavy projects easier to manage by providing an accessible interface
backed by a centralized, user-defined database of relevant information. The goal is to promote consistency in information and ease in
the writer workflow by prioritizing user-friendliness. Information and calculations can be accessed through Discord commands,
and lore data is stored in a simple Google Sheet, making the bot's use approachable even to non-programmers. 

## Installation

1. Install [Python](https://www.python.org/downloads/), then use [pip](https://pip.pypa.io/en/stable/) to install Lore Bot's dependencies:

```bash
pip install discord
pip install gspread
pip install pandas
pip install oauth2client
pip install requests
```

2. Follow [these steps](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to create a Discord Bot. Open `bot_token.py` and put in your Bot Token.

3. On Google Drive, create the Sheet you'd like to use as the database and call it "LoreBot Database". At the bottom of the page, rename the current sheet to "Characters". The database must have a column titled Name (which the bot will use to look up characters), but all other columns are up to you.

4. Follow [these steps](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html) to allow your bot access to your Sheet. Download the credentials file and place it in the root Lore Bot folder. Make sure its name is `api_keys.json`.

5. Run Lore Bot and enjoy.
```bash
python3 ./LoreBot.py
```

## Usage

Once the bot has been set up, simply use the following commands in a Discord channel it has access to:
| Command    | Arguments             | Usage  |
| ---------- | --------------------- | ------ |
| !hello     |  | Says hello! |
| !help      |  | Lists all commands. |
| !lookup    | (name) (attribute) | Looks up the given attribute about a character. |
| !findall   | (attribute) (content) | Lists all characters matching the specified attribute. |
| !count     | (attribute) | Returns a list of the number of occurrences of each unique entry for the given attribute. |
| !total     |  | Returns the total number of characters in the database. |
| !bio       | (name) | Returns the entire database entry for the specified character. |
| !agecalc   | (name) (year) | Calculates how old the given character would be in the given year. (Requires a field titled Birthyear in the database.) |
| !yearcalc  | (name) (age) | Calculates the year when the given character would be the given age. (Requires a field titled Birthyear in the database.)|
| !agegap    | (name1) (name2) | Calculates the age gap in years between the two given characters. (Requires a field titled Birthyear in the database.) |
| !agewhen   | (name1) when (name2) (age) | Calculates the age the first character would be when the second character is the given age. (Requires a field titled Birthyear in the database.) |
| !related   | (name1) (name2) | Checks all family relations and returns true if characters are related in any way. (Requires fields titled Parents and Spouses in the database.) |

## License
[MIT](https://choosealicense.com/licenses/mit/)