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

def get_db():
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
    return(data)

def get_attribute(name, attribute, data):
    data.columns = data.columns.str.lower()
    # mask out the row we need
    mask = data['name'].str.lower()==name.lower()
    # return the requested attribute from the masked row
    att = str(data[mask][attribute.lower()].values[0])
    return att

def get_names(attribute, content, data):
    data.columns = data.columns.str.lower()
    # mask out the rows we need
    #(Parents requires searching for a substring and not a perfect match)
    if attribute.lower() == 'parents':
        mask = data[attribute.lower()].str.contains(content.capitalize())
    else:
        mask = data[attribute.lower()].str.lower()==content.lower()
    # return the requested names from the masked rows
    names = data[mask]['name'].values.tolist()
    return names

def get_count(column, data):
    data.columns = data.columns.str.lower()
    # output the count of each unique value in the specified column
    return data[column].value_counts().to_string(header=True, length=False, dtype=False, name=False, max_rows=None).replace('    ',': ')

def get_total(data):
    return str(len(data.index))

def get_row(name, data):
    # isolate the desired row, convert it to a dict of type records to remove the index
    # from the value fields, then "unwrap" the dict from records format by extracting it
    row_dict = data[data['Name'].str.lower()==name.lower()].to_dict(orient='records')[0]
    return str("\n".join("**{}:** {}".format(k, v) for k, v in row_dict.items()))

def get_age(name, test_year, data):
    birth_year = int(get_attribute(name, 'birthyear', data))
    test_year = int(test_year)
    if test_year >= birth_year:
        age = test_year - birth_year
        if age != 1:
            return ('In ' + str(test_year) + ', ' + name.capitalize() + ' would be ' + str(age) + ' years old.')
        else:
            return ('In ' + str(test_year) + ', ' + name.capitalize() + ' would be ' + str(age) + ' year old.')
    else:
        age = birth_year - test_year
        if age != 1:
            return (str(test_year) + ' was ' + str(age) + ' years before ' + name.capitalize() + ' was born.')
        else:
            return (str(test_year) + ' was ' + str(age) + ' year before ' + name.capitalize() + ' was born.')

def get_year(name, age, data):
    birth_year = int(get_attribute(name, 'birthyear', data))
    age = int(age)
    return str(birth_year + age)

def get_age_gap(name1, name2, data):
    birth1 = int(get_attribute(name1, 'birthyear', data))
    birth2 = int(get_attribute(name2, 'birthyear', data))
    gap = birth1 - birth2
    if gap > 0:
        return str(name1).capitalize() + ' is ' + str(gap) + ' years younger than ' + str(name2).capitalize() + '.'
    elif gap < 0:
        return str(name1).capitalize() + ' is ' + str(abs(gap)) + ' years older than ' + str(name2).capitalize() + '.'
    else:
        return str(name1).capitalize() + ' and ' + str(name2).capitalize() + ' are the same age.'

def get_age_when(name1, name2, age2, data):
    birth1 = int(get_attribute(name1, 'birthyear', data))
    birth2 = int(get_attribute(name2, 'birthyear', data))
    gap = birth1 - birth2
    age1 = int(age2) - gap
    return age1

def get_family(name1, data):
    parents = get_attribute(name1, 'Parents', data).split(', ')
    siblings = []
    for i in parents:
        if i != '':
            siblings += get_names('Parents', i, data)
    #remove duplicates from siblings list
    siblings = list(set(siblings))
    spouses = get_attribute(name1, 'Spouse', data).split(', ')
    children = get_names('Parents', name1, data)
    #clear any empty strings
    parents = [x for x in parents if x]
    spouses = [x for x in spouses if x]
    return parents + siblings + spouses + children

def check_family(name1, name2, data):
    if name2 in get_family(name1, data):
        return True
    else:
        return False

def are_related(name1, name2, data):
    unchecked = [name1]
    checked = []
    related = False
    while len(unchecked) != 0:
        if check_family(unchecked[0], name2, data) == True:
            related = True
            break
        else:
            checked.append(unchecked[0])
            for n in get_family(unchecked[0], data):
                if n not in checked:
                    unchecked.append(n)
            unchecked.pop(0)
            #clear unchecked of any empty strings and remove duplicates
            unchecked = [x for x in unchecked if x]
            unchecked = list(set(unchecked))
    return(related)

#def factorial(n):
#    if n == 0:
#        return 1
#    else:
#        return n * factorial(n-1)

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
    if message.content.startswith('!say '):
        arg_pos = message.content.find(' ')
        msg = 'Okay, I\'m saying ' + message.content[arg_pos + 1:]
        await message.channel.send(msg)
        
    # look up an attribute value in a specific row on the Google sheet
    if message.content.startswith('!lookup '):
        args = message.content.split()
        try:
            msg = args[1].capitalize() + '\'s ' + args[2] + ' is: ' + get_attribute(args[1], args[2], get_db())
        except:
            msg = 'That lookup is invalid, try again. Available attributes are:\n`' + str("`".join("{}` ".format(v) for v in get_db().columns.values.tolist()))
        finally:
            await message.channel.send(msg)

    # return a count of each unique value in a specified column of the Google sheet
    if message.content.startswith('!count '):
        args = message.content.split()
        forbidden = ['name', 'pic', 'birthday', 'height']
        if args[1].lower() not in forbidden:
            msg = get_count(args[1], get_db())
            await message.channel.send('Here is the ' + args[1] + ' count:\n' + msg)
        else:
            await message.channel.send('Sorry, you can\'t count by ' + args[1] + 's. Try another attribute instead.')

    # returns the total number of entries in the Google sheet
    if message.content.startswith('!total'):
        msg = get_total(get_db())
        await message.channel.send('The total character count is: ' + msg)

    # returns an entire row from the Google sheet, located via Name
    if message.content.startswith('!bio '):
        args = message.content.split()
        msg = get_row(args[1], get_db())
        await message.channel.send(args[1].capitalize() + '\'s Bio: \n' + msg)

    # compare a character's birth year to the given year
    if message.content.startswith('!agecalc '):
        args = message.content.split()
        msg = get_age(args[1], args[2], get_db())
        await message.channel.send(msg)

    # calculate the year from a character's age
    if message.content.startswith('!yearcalc '):
        args = message.content.split()
        year = get_year(args[1], args[2], get_db())
        await message.channel.send(args[1].capitalize() + ' would be ' + args[2] + ' in the year ' + year + '.')

    # compare two characters' birth years
    if message.content.startswith('!agegap '):
        args = message.content.split()
        try:
            msg = get_age_gap(args[1], args[2], get_db())
        except:
            msg = 'There was a problem looking up one of the characters, or that character doesn\'t have a valid birth year.'
        finally:
            await message.channel.send(msg)

    # calculate a character's age in relation to another character's age
    if message.content.startswith('!agewhen '):
        args = message.content.split()
        try:
            msg = args[1].capitalize() + ' would be ' + str(get_age_when(args[1], args[3], args[4], get_db())) + ' when ' + args[3].capitalize() + ' is ' + args[4] + '.'
        except:
            msg = 'There was a problem looking up one of the characters, or that character doesn\'t have a valid birth year.'
        finally:
            await message.channel.send(msg)
    
    # look up all names with a specified common attribute
    if message.content.startswith('!findall '):
        args = message.content.split()
        try:
            if len(get_names(args[1], args[2], get_db())) != 0:
                msg = 'Here are all characters with a ' + args[1].capitalize() + ' matching ' + args[2] + ':\n' + str("".join("{}\n".format(v) for v in get_names(args[1], args[2], get_db())))
            else:
                msg = 'There are no characters with a ' + args[1].capitalize() + ' matching ' + args[2] + '.'
        except:
            msg = 'That attribute is invalid. Available attributes are:\n`' + str("`".join("{}` ".format(v) for v in get_db().columns.values.tolist()))
        finally:
            await message.channel.send(msg)
    
    # check if two given characters are related
    if message.content.startswith('!related'):
        args = message.content.split()
        try:
            if are_related(args[1].capitalize(), args[2].capitalize(), get_db()):
                msg = args[1].capitalize() + ' and ' + args[2].capitalize() + ' are related.'
            else:
                msg = args[1].capitalize() + ' and ' + args[2].capitalize() + ' are not related.'
        except:
            msg = 'There was a problem looking up one of the characters. Check your spelling and try again.'
        finally:
            await message.channel.send(msg)

    # list commands when a user asks for help
    if message.content.startswith('!help'):
        cmd_list = ['!hello', '!say (text)', '!lookup (name) (attribute)', '!findall (attribute) (content)', '!count (attribute)', '!total', '!bio (name)', '!agecalc (name) (year)', '!yearcalc (name) (age)', '!agegap (name1) (name2)', '!agewhen (name1) when (name2) (age)', '!related (name1) (name2)']
        await message.channel.send('These are the commands I can process:\n`' + str("`".join("{}`\n".format(v) for v in cmd_list)))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Start the BOT!
client.run(BOT_TOKEN)

