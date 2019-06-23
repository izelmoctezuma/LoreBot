# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import discord
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


BOT_TOKEN = "NTkyMTkyNDU5NTc2OTY3MTY4.XQ7xYg.LM4irLYwS6oNdLLeyhgIx6Zyw74"

client = discord.Client()   

def get_data(name, attribute):
    # Google Sheet access
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    google_key = '/Users/paolamoctezuma/PythonDev/DMBot/api-keys.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_key, scope)
    client = gspread.authorize(creds)
    sheet = client.open('DMBot Database')
    wsheet = sheet.worksheet('Characters')
    
    # Extract all the values - this returns a dictionary
    sheet1_data = wsheet.get_all_records()
    data = pd.DataFrame(sheet1_data)
    data.columns = data.columns.str.lower()
    mask = data['name'].str.lower()==name.lower()
    return data[mask][attribute.lower()].values[0]

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('!hello'):
        msg = 'Hello, {0.author.mention}!'.format(message)
        await message.channel.send(msg)
    if message.content.startswith('!say'):
        arg_pos = message.content.find(' ')
        msg = 'Okay, I\'m saying ' + message.content[arg_pos + 1:]
        await message.channel.send(msg)
    if message.content.startswith('!lookup'):
            args = message.content.split()
            msg = get_data(args[1], args[2])
            await message.channel.send(args[1]+ '\'s ' + args[2] + ' is: ' + msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Start the BOT!
client.run(BOT_TOKEN)

