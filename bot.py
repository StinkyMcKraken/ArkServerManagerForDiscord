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
        await message.channel.send('What\'s Krackin\'?')

    #help command
    elif message.content.startswith('$help'):
        helpmessage = """This version is super dumb and basic.
WARNING THERE IS NO IDIOT PROOFING WITH THE FOLLOWING COMMANDS
---
$hello - simple response test
$help - this message
$start <server> - starts <server> instance
$stop <server> - stops <server> instance.
                Instant stop, no check for connected players
$restart <server> - stops then starts <server>.
                   Instant stop, no check for players
$force update - invokes LGSM forced update. All running servers
                are given 10 minute notification, stopped,
                updated, and restarted
$update lgsm - updates LGSM itself on all instances. Should not be
               necessary but may be needed if other commands fail.
               Does not stop servers

Valid <server>s at this time:
   island
   genesis
   aberration
   ragnarok
"""
        await message.channel.send(helpmessage)

    #ark force update
    elif message.content.startswith('$force update'):
        rc = subprocess.run("/home/ark/scripts/multipleupdate.sh", capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #ark update lgsm
    elif message.content.startswith('$update lgsm'):
        rc = subprocess.run(["/home/ark/arkserver", "update-lgsm"], capture_output=True, text=True)
        rc = subprocess.run(["/home/ark/island", "update-lgsm"], capture_output=True, text=True)
        rc = subprocess.run(["/home/ark/aberration", "update-lgsm"], capture_output=True, text=True)
        rc = subprocess.run(["/home/ark/genesis", "update-lgsm"], capture_output=True, text=True)
        rc = subprocess.run(["/home/ark/crystal", "update-lgsm"], capture_output=True, text=True)
        rc = subprocess.run(["/home/ark/ragnarok", "update-lgsm"], capture_output=True, text=True)
        await message.channel.send("LGSM updated on all instances")

    #start genesis server
    elif message.content.startswith('$start genesis'):
        rc = subprocess.run(["/home/ark/genesis", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop genesis server
    elif message.content.startswith('$stop genesis'):
        rc = subprocess.run(["/home/ark/genesis", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart genesis Server
    elif message.content.startswith('$restart genesis'):
        rc = subprocess.run(["/home/ark/genesis", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #start island server
    elif message.content.startswith('$start island'):
        rc = subprocess.run(["/home/ark/island", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop island server
    elif message.content.startswith('$stop island'):
        rc = subprocess.run(["/home/ark/island", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart island Server
    elif message.content.startswith('$restart island'):
        rc = subprocess.run(["/home/ark/island", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #start aberration server
    elif message.content.startswith('$start aberration'):
        rc = subprocess.run(["/home/ark/aberration", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop aberration server
    elif message.content.startswith('$stop aberration'):
        rc = subprocess.run(["/home/ark/aberration", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart aberration Server
    elif message.content.startswith('$restart aberration'):
        rc = subprocess.run(["/home/ark/aberration", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #start ragnarok server
    elif message.content.startswith('$start ragnarok'):
        rc = subprocess.run(["/home/ark/ragnarok", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop ragnarok server
    elif message.content.startswith('$stop ragnarok'):
        rc = subprocess.run(["/home/ark/ragnarok", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart ragnarok Server
    elif message.content.startswith('$restart ragnarok'):
        rc = subprocess.run(["/home/ark/ragnarok", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    else:
        await message.channel.send("Krak off, you'r kiddin' me!!")
        #C to K error, please remedy
        #C to K?
        #problem exists between Chair and Keyboard. Please examine and remedy, you dumdum

    print(f'{message.author}:::{message.content}')  #echo message to console (debug)

client.run(TOKEN)       #actually start the Discord session
