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
$start <server> - you need an explanation ?
$stop <server> - Instant stop, no check for connected players
$restart <server> - stops then starts <server>.
                   Instant stop, no check for players
$force update - invokes LGSM forced update. All running servers
                are given 10 minute notification, stopped,
                updated, and restarted
$update lgsm - updates LGSM itself on all instances. Should not be
               necessary but may be needed if other commands fail.
               Does not stop servers

Valid <server> at this time:
   island       27001
   aberration   27002
   ragnarok     27003
   scorched     27004
   center       27005
   crystal      27006
   extinction   27007
   valguero     27008
   genesis      27009
"""
        await message.channel.send(helpmessage)

    #ark force update
    elif message.content.startswith('$force update'):
        await message.channel.send("Starting Forced Update in-game notification script. Please wait 15 minutes for update and restart to complete.")
        rc = subprocess.run("/home/ark/scripts/multipleupdate.sh", capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr + "\nUpdate and Restart complete.")

    #ark update lgsm
    elif message.content.startswith('$update lgsm'):
        rc = subprocess.run(["/home/ark/arkserver", "update-lgsm"])
        rc = subprocess.run(["/home/ark/island", "update-lgsm"])
        rc = subprocess.run(["/home/ark/aberration", "update-lgsm"])
        rc = subprocess.run(["/home/ark/ragnarok", "update-lgsm"])
        rc = subprocess.run(["/home/ark/scorched", "update-lgsm"])
        rc = subprocess.run(["/home/ark/center", "update-lgsm"])
        rc = subprocess.run(["/home/ark/crystal", "update-lgsm"])
        rc = subprocess.run(["/home/ark/extinction", "update-lgsm"])
        rc = subprocess.run(["/home/ark/valguero", "update-lgsm"])
        rc = subprocess.run(["/home/ark/genesis", "update-lgsm"])
        await message.channel.send("LGSM updated on all instances")

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

    #start scorched earth server
    elif message.content.startswith('$start scorched'):
        rc = subprocess.run(["/home/ark/scorched", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop scorched earth server
    elif message.content.startswith('$stop scorched'):
        rc = subprocess.run(["/home/ark/scorched", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart scorched earth Server
    elif message.content.startswith('$restart scorched'):
        rc = subprocess.run(["/home/ark/scorched", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #start the center server
    elif message.content.startswith('$start center'):
        rc = subprocess.run(["/home/ark/center", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop the center server
    elif message.content.startswith('$stop center'):
        rc = subprocess.run(["/home/ark/center", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart the center Server
    elif message.content.startswith('$restart center'):
        rc = subprocess.run(["/home/ark/center", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #start crystal isles server
    elif message.content.startswith('$start crystal'):
        rc = subprocess.run(["/home/ark/crystal", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop crystal isles server
    elif message.content.startswith('$stop crystal'):
        rc = subprocess.run(["/home/ark/crystal", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart crystal isles Server
    elif message.content.startswith('$restart crystal'):
        rc = subprocess.run(["/home/ark/crystal", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #start extinction server
    elif message.content.startswith('$start extinction'):
        rc = subprocess.run(["/home/ark/extinction", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop extinction server
    elif message.content.startswith('$stop extinction'):
        rc = subprocess.run(["/home/ark/extinction", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart extinction Server
    elif message.content.startswith('$restart extinction'):
        rc = subprocess.run(["/home/ark/extinction", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #start valguero server
    elif message.content.startswith('$start valguero'):
        rc = subprocess.run(["/home/ark/valguero", "start"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #stop valguero server
    elif message.content.startswith('$stop valguero'):
        rc = subprocess.run(["/home/ark/valguero", "stop"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

    #restart valguero Server
    elif message.content.startswith('$restart valguero'):
        rc = subprocess.run(["/home/ark/valguero", "restart"], capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n" + rc.stderr)

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

    else:
        await message.channel.send("Krak off, you'r kiddin' me!!")
        #C to K error, please remedy
        #C to K?
        #problem exists between Chair and Keyboard. Please examine and remedy, you dumdum

    print(f'{message.author}:::{message.content}')  #echo message to console (debug)

client.run(TOKEN)       #actually start the Discord session
