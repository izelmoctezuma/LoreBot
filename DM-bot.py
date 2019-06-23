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
    
    # extract all the values - this returns a dictionary
    sheet1_data = wsheet.get_all_records()
    data = pd.DataFrame(sheet1_data)
    data.columns = data.columns.str.lower()
    
    # mask out the row we need
    mask = data['name'].str.lower()==name.lower()
    
    # return the requested attribute from the masked row
    return data[mask][attribute.lower()].values[0]


def get_count(column):
    # Google Sheet access
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    google_key = '/Users/paolamoctezuma/PythonDev/DMBot/api-keys.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_key, scope)
    client = gspread.authorize(creds)
    sheet = client.open('DMBot Database')
    wsheet = sheet.worksheet('Characters')
    
    # extract all the values - this returns a dictionary
    sheet1_data = wsheet.get_all_records()
    data = pd.DataFrame(sheet1_data)
    data.columns = data.columns.str.lower()
    
    # output the count of each unique value in the specified column
    return data[column].value_counts().to_string(header=True, length=False, dtype=False, name=False, max_rows=None).replace('    ',': ')

def get_total():
    # Google Sheet access
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    google_key = '/Users/paolamoctezuma/PythonDev/DMBot/api-keys.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_key, scope)
    client = gspread.authorize(creds)
    sheet = client.open('DMBot Database')
    wsheet = sheet.worksheet('Characters')
    
    # extract all the values - this returns a dictionary
    sheet1_data = wsheet.get_all_records()
    data = pd.DataFrame(sheet1_data)
    data.columns = data.columns.str.lower()
    
    return str(len(data.index))


def get_row(name):
    # Google Sheet access
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    google_key = '/Users/paolamoctezuma/PythonDev/DMBot/api-keys.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_key, scope)
    client = gspread.authorize(creds)
    sheet = client.open('DMBot Database')
    wsheet = sheet.worksheet('Characters')
    
    # extract all the values - this returns a dictionary
    sheet1_data = wsheet.get_all_records()
    data = pd.DataFrame(sheet1_data)
    
    # isolate the desired row, convert it to a dict of type records to remove the index
    # from the value fields, then "unwrap" the dict from records format by extracting it
    row_dict = data[data['Name'].str.lower()==name.lower()].to_dict(orient='records')[0]
    return str("\n".join("**{}:** {}".format(k, v) for k, v in row_dict.items()))


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # say hi
    if message.content.startswith('!hello'):
        msg = 'Hello, {0.author.mention}!'.format(message)
        await message.channel.send(msg)
    # copy what the user says
    if message.content.startswith('!say'):
        arg_pos = message.content.find(' ')
        msg = 'Okay, I\'m saying ' + message.content[arg_pos + 1:]
        await message.channel.send(msg)
    # look up an attribute value in a specific row on the Google sheet
    if message.content.startswith('!lookup'):
        args = message.content.split()
        msg = get_data(args[1], args[2])
        await message.channel.send(args[1] + '\'s ' + args[2] + ' is: ' + msg)
    # return a count of each unique value in a specified column of the Google sheet
    if message.content.startswith('!count'):
        args = message.content.split()
        forbidden = ['name', 'pic', 'birthday', 'height']
        if args[1].lower() not in forbidden :
            msg = get_count(args[1])
            await message.channel.send('Here is the ' + args[1] + ' count:\n' + msg)
        else:
            await message.channel.send('Sorry, you can\'t count by ' + args[1] + 's. Try another attribute instead.')
    # returns the total number of entries in the Google sheet
    if message.content.startswith('!total'):
        msg = get_total()
        await message.channel.send('The total character count is: ' + msg)
    # returns an entire row from the Google sheet, located via Name
    if message.content.startswith('!bio'):
        args = message.content.split()
        msg = get_row(args[1])
        await message.channel.send(args[1] + '\'s Bio: \n' + msg)
            
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Start the BOT!
client.run(BOT_TOKEN)

