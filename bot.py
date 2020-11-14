# bot.py
import os

#documentation for discord.py is at https://discordpy.readthedocs.io/en/latest/

import discord      #import discord.py library
import subprocess   #import subprocess library
from dotenv import load_dotenv      #import function from dotenv library

# Test for existence of file .env where info like the token for Discord is held
# Do not want to hard code the Discord token here, this file is public on GitHub

# The Discord Token is essentially the bot's login credential for Discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  #get Discord token from .env file

client = discord.Client()       #create Discord object


############################################################
# Need to determine a way for this script to know what valid server launchers
# are available.  LinuxGSM allows multiple intances off the same installation
# of ARK. Each instance is managed by a copy of the server launcher script
# with different names. In my case, the server launchers are named after The
# vaious maps, so 'island', 'scorched', 'crystal', etc.
#
# maybe the best option would be to utilize the .env file and manually provide
# a list of valid executables. Maybe there is a better way to import external
# data into this script, maybe xml or a .ini file?
#############################################################


#############################################################
#############################################################
##  THIS IS A STRIPPED DOWN VERY BASIC COMMAND LINE TO MAKE STUFF WORK
#############################################################
#############################################################



@client.event
async def on_ready():           #when Discord session is ready, echo status to console
    print(
        f'{client.user} has connected to Discord!\n'
        f'{client.user} is connected to the following guild:\n'
)
    for guild in client.guilds:     #list channels we are linked to
        print(f'{guild.name}(id: {guild.id})\n')

@client.event
async def on_message(message):    #when a message is received in the channel
    if message.author == client.user:   #ignore messages from myself
        return

    if not(message.content.startswith('$')):  #ignore messages not starting with '$'
        return

    #equivalent to hello world
    if message.content.startswith('$hello'):
        await message.channel.send('What\'s Crackin\'?')

    #help command
    elif message.content.startswith('$help'):
        helpmessage = """This version is super dumb and basic.
WARNING THERE IS NO IDIOT PROOFING WITH THE FOLLOWING COMMANDS
---
$hello - simple response test
$help - this message
$start genesis - starts Genesis instance
$stop genesis - stops Genesis instance.  Instant stop, no check for connected players
$update genesis - invokes standard LGSM update with version check. Server only stopped if update is available
$force genesis - invokes LGSM forced update. Server is stopped, updated, and restarted
$update lgsm - updates LGSM itself. Should not be necessary but may be needed if other commands fail
"""
        await message.channel.send(helpmessage)

    #start ark server command
    elif message.content.startswith('$start genesis'):
        rc = subprocess.run(["/home/ark/genesis", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop ark server command
    elif message.content.startswith('$stop genesis'):
        rc = subprocess.run(["/home/ark/genesis", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #ark server update
    elif message.content.startswith('$update genesis'):
        rc = subprocess.run(["/home/ark/genesis", "update"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #ark force update
    elif message.content.startswith('$force genesis'):
        rc = subprocess.run(["/home/ark/arkserver", "fu"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #ark update lgsm
    elif message.content.startswith('$update lgsm'):
        rc = subprocess.run(["/home/ark/genesis", "update-lgsm"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    print(f'{message.author}:::{message.content}')  #echo message to console (debug)

client.run(TOKEN)       #actually start the Discord session
