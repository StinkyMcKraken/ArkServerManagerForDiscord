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
# a list of valid executables.
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

    #create a test file
    elif message.content.startswith('$touch'):
        rc = subprocess.call("/home/ark/discordbot/touch.sh")
        await message.channel.send(rc)

    #start ark server command
    elif message.content.startswith('$ark start'):
        rc = subprocess.call("/home/ark/arkserver", "start")
        #want to figure out how to run a bash script, capture stdout from that
        #script and post the stdout back to Discord as a reply to the command
        #Would be really cool to capture the stdout in real time as the script
        #is in progress and update the Discord post with additional info

    #stop ark server command
    elif message.content.startswith('$ark stop'):
        rc = subprocess.call("/home/ark/arkserver", "stop")

    #ark server update
    elif message.content.startswith('$ark update'):
        rc = subprocess.call("/home/ark/arkserver", "update")

    #ark force update
    elif message.content.startswith('$ark force update'):
        rc = subprocess.call("/home/ark/arkserver", "fu")

    #ark update lgsm
    elif message.content.startswith('$ark update lgsm'):
        rc = subprocess.call("/home/ark/arkserver", "update-lgsm")

    print(f'{message.author}:::{message.content}')  #echo message to console (debug)

client.run(TOKEN)       #actually start the Discord session
