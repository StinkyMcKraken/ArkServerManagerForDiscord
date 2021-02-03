# bot.py
import os

# documentation for discord.py is at https://discordpy.readthedocs.io/en/latest/

import discord      # import discord.py library
import subprocess   # import subprocess library
import random       # import random library
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
async def on_message(message):    # when a message is received in the channel
    if message.author == client.user:   #ignore messages from myself
        return

    if not(message.content.startswith('$')):  # ignore messages not starting with '$'
        return

    # equivalent to hello world
    if message.content.startswith('$hello'):
        await message.channel.send('What\'s Krackin\'?')

    # help command
    elif message.content.startswith('$help'):
        helpmessage = """This version is super dumb and basic.
WARNING THERE IS NO IDIOT PROOFING WITH THE FOLLOWING COMMANDS
BEST TO LET ONE COMMAND COMPLETE BEFORE STARTING ANOTHER
---
**$hello** -
simple response test

**$help** -
this message

**$status** -
lists all running servers and players connected

**$start <server>** -
you need an explanation ?

**$stop <server>** -
Instant stop, no check for connected players

**$restart <server>** -
stops then starts <server>. Instant stop, no check for players

**$force update** -
invokes LGSM forced update. All running servers are given 10 minute notification, stopped, updated, and restarted.
*Cheat mode*: if you manually stop all running servers prior to running this command, it will skip the 10 minute notification process. Servers will need to be manually restarted after the update.

**$backup** -
invokes LGSM backup. All running servers are given 10 minute notification, stopped, backedup, updated, and restarted. Same cheat as $force update

**$update lgsm** -
updates LGSM itself on all instances. Should not be necessary but may be needed if other commands fail. Does not stop servers


**Valid <server> at this time**:
27001 island
27002 aberration
27003 ragnarok
27004 scorched
27005 center
27006 crystal
27007 extinction
27008 valguero
27009 genesis
27011 arkadmin (island)
"""
        await message.channel.send(helpmessage)

    # bot server status
    elif message.content.startswith('$status'):
        rc = subprocess.run("/home/ark/scripts/status.sh", capture_output=True, text=True)
        await message.channel.send(rc.stdout + "\n")

    # ark force update
    elif message.content.startswith('$force update'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
#            somethingrunning = True
            await message.channel.send("Starting Forced Update in-game notification script. Please wait 15 minutes for update and restart to complete.")
            rc = subprocess.run("/home/ark/scripts/multipleupdate.sh", capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr + "\nUpdate and Restart complete.")
#            somethingrunning = False

    # ark backup
    elif message.content.startswith('$backup'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
#            somethingrunning = True
            await message.channel.send("Starting Backup in-game notification script. Please wait 30-40 minutes for backup, update, and restart to complete.")
            rc = subprocess.run("/home/ark/scripts/multiplebackup.sh", capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr + "\nbot.py: Backup, Update, and Restart complete.")
#            somethingrunning = False

    # ark update lgsm
    elif message.content.startswith('$update lgsm'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
#            somethingrunning = True
            await message.channel.send("**:Updating LGSM:**")
            rc = subprocess.run(["/home/ark/arkserver", "update-lgsm"])
            await message.channel.send(rc.stdout)
            rc = subprocess.run(["/home/ark/island", "update-lgsm"])
            rc = subprocess.run(["/home/ark/aberration", "update-lgsm"])
            rc = subprocess.run(["/home/ark/ragnarok", "update-lgsm"])
            rc = subprocess.run(["/home/ark/scorched", "update-lgsm"])
            rc = subprocess.run(["/home/ark/center", "update-lgsm"])
            rc = subprocess.run(["/home/ark/crystal", "update-lgsm"])
            rc = subprocess.run(["/home/ark/extinction", "update-lgsm"])
            rc = subprocess.run(["/home/ark/valguero", "update-lgsm"])
            rc = subprocess.run(["/home/ark/genesis", "update-lgsm"])
            await message.channel.send("**:LGSM updated on all instances:**")
#            somethingrunning = False

    # start island server
    elif message.content.startswith('$start island'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/island", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop island server
    elif message.content.startswith('$stop island'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/island", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart island Server
    elif message.content.startswith('$restart island'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/island", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start aberration server
    elif message.content.startswith('$start aberration'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/aberration", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop aberration server
    elif message.content.startswith('$stop aberration'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/aberration", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart aberration Server
    elif message.content.startswith('$restart aberration'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/aberration", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start ragnarok server
    elif message.content.startswith('$start ragnarok'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/ragnarok", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop ragnarok server
    elif message.content.startswith('$stop ragnarok'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/ragnarok", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart ragnarok Server
    elif message.content.startswith('$restart ragnarok'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/ragnarok", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start scorched earth server
    elif message.content.startswith('$start scorched'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/scorched", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop scorched earth server
    elif message.content.startswith('$stop scorched'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/scorched", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart scorched earth Server
    elif message.content.startswith('$restart scorched'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/scorched", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start the center server
    elif message.content.startswith('$start center'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/center", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop the center server
    elif message.content.startswith('$stop center'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/center", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart the center Server
    elif message.content.startswith('$restart center'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/center", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start crystal isles server
    elif message.content.startswith('$start crystal'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/crystal", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop crystal isles server
    elif message.content.startswith('$stop crystal'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/crystal", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart crystal isles Server
    elif message.content.startswith('$restart crystal'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/crystal", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start extinction server
    elif message.content.startswith('$start extinction'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/extinction", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop extinction server
    elif message.content.startswith('$stop extinction'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/extinction", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart extinction Server
    elif message.content.startswith('$restart extinction'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/extinction", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start valguero server
    elif message.content.startswith('$start valguero'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/valguero", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop valguero server
    elif message.content.startswith('$stop valguero'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/valguero", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart valguero Server
    elif message.content.startswith('$restart valguero'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/valguero", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start genesis server
    elif message.content.startswith('$start genesis'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/genesis", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop genesis server
    elif message.content.startswith('$stop genesis'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/genesis", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart genesis Server
    elif message.content.startswith('$restart genesis'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/genesis", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # start arkadmin server
    elif message.content.startswith('$start arkadmin'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/arkadmin", "start"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # stop arkadmin server
    elif message.content.startswith('$stop arkadmin'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/arkadmin", "stop"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # restart arkadmin Server
    elif message.content.startswith('$restart arkadmin'):
#        if somethingrunning:
#            await message.channel.send("Please wait for previous command to finish")
#        else:
            rc = subprocess.run(["/home/ark/arkadmin", "restart"], capture_output=True, text=True)
            await message.channel.send(rc.stdout + "\n" + rc.stderr)

    # unknown command, return random error message
    else:
        error_quotes = [
            "Krak off, you\'r kiddin\' me!!",
            "C to K error, please remedy",
            "EEP!",
            "Problem exists between Chair and Keyboard. Please examine and remedy, you dumdum",
            "I know not what this is you speak of",
            "Crap!"
            "f*k"
            "Black magic, the allure it tempting.  It's easy, and fun, like Legos"
        ]
        response = random.choice(error_quotes)
        await message.channel.send(response)

    #print(f'{message.author}:::{message.content}')  #echo message to console (debug)

# variable to detect if another command is running.  cannot have multiple
# commands overlapping themselves.
#somethingrunning = False

client.run(TOKEN)       #actually start the Discord session
