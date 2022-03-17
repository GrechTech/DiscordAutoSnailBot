import re
import os 
from discord.ext import commands
import time

# Config constants
TOKEN = ""
TriggerDays = 3

# Working directory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
URLS_PATH = os.path.join(DIR_PATH,"urls.txt")

# Auto Snail find URL
def FindURL(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]


# Discord functionality
def check_reply(message):
    if message.reference is not None and message.is_system :
        print(message.reference)
        return True
    return False

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    global lastConsole
    if message.author == bot.user: 
        return

    if not check_reply(message):
        # Autosnail
        urls = FindURL(message.content)
        # Check message for url
        if len(urls) > 0:
            for url in urls:
                snail = False
                clean_url = url.split("?")[0].lower().rstrip()
                newlines = []
                # Check each line of file
                with open(URLS_PATH, 'r') as file:
                    for line in file:
                        clean_line = line.rstrip()
                        date = int(clean_line.split('>')[0])
                        lineurl = clean_line.split('>')[1]
                        # Check if message within last 3 days
                        if (int(time.time()) - date) < (86400 * TriggerDays):
                            newlines.append(clean_line) # Create new list with in date messages
                            if lineurl == clean_url: # If message a Snail
                                snail = True        

                # Create new file with only in date messages   
                with open(URLS_PATH, 'w') as file:
                    for item in newlines:
                        file.write("%s\n" % item) 

                # Snail if snailable, else add to list
                if snail:
                    emoji = '\U0001F40C' #Snail
                    await message.add_reaction(emoji)
                else:
                    with open(URLS_PATH, 'a') as file:
                        newline = str(int(time.time())) + '>' + clean_url + '\n'
                        file.write(newline)

    await bot.process_commands(message)

# Start
bot.run(TOKEN)
