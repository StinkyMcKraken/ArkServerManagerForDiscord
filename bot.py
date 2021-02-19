# bot.py
import os

# Discord Bot for start/stop/update Ark Servers via Discord

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
async def runprocesstodiscord(cmd, output, message):
    rcmessage = await message.channel.send(output)
    rc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Poll process for new output until finished
    while True:
        nextline = rc.stdout.readline()
        if nextline == '' and rc.poll() is not None:
            break
        #print(f'{nextline}')  #echo message to console (debug)
        output = output + nextline
        if len(output) > 2000:
            output = nextline
            rcmessage = await message.channel.send(output)
        else:
            await rcmessage.edit(content=output)

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

**Use $% to show servers list**
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

    elif message.content.startswith('$%'):
        helpmessage="""**Valid <server> at this time**:
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
        rc = subprocess.run("/home/ark/scripts/status.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # ark force update
    elif message.content.startswith('$force update'):
        await runprocesstodiscord(
            "/home/ark/scripts/multipleupdate.sh",
            "Starting Forced Update in-game notification script. Please wait 15 minutes for update and restart to complete.\n",
            message)
        await message.channel.send("__**Update and Restart complete.**__")

    # ark backup
    elif message.content.startswith('$backup'):
        await runprocesstodiscord(
            "/home/ark/scripts/multiplebackup.sh",
            "Starting Backup in-game notification script. Please wait 30-40 minutes for backup, update, and restart to complete.\n",
            message)
        await message.channel.send("__**Backup, Update, and Restart complete.**__")

    # send kick command to given instance
    # usage: $kick <server> <playerID>
    elif message.content.startswith('$kick '):
        kickargs = message.content.split(" ")
        # test if $kick command was supplied with two arguments
        if len(kickargs[1]) = 0 or len(kickargs[2]) = 0:
            await message.channel.send("Usage: $kick <server> <playersteamid>")
        else
            rc = subprocess.run(["/home/ark/rcon", kickargs[1], "KickPlayer " + kickargs[2]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            await message.channel.send(rc.stdout)

    # ark update lgsm
    elif message.content.startswith('$update lgsm'):
        await runprocesstodiscord(
            "/home/ark/arkserver ul",
            "__**:Updating LGSM:**__\n",
            message)
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/island"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/aberration"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/ragnarok"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/scorched"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/center"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/crystal"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/extinction"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/valguero"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/genesis"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/genesis2"])
        rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/arkadmin"])
        await message.channel.send("**:LGSM updated on all instances:**")

    # start island server
    elif message.content.startswith('$start island'):
        rc = subprocess.run(["/home/ark/island", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop island server
    elif message.content.startswith('$stop island'):
        rc = subprocess.run(["/home/ark/island", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart island Server
    elif message.content.startswith('$restart island'):
        rc = subprocess.run(["/home/ark/island", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start aberration server
    elif message.content.startswith('$start aberration'):
        rc = subprocess.run(["/home/ark/aberration", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop aberration server
    elif message.content.startswith('$stop aberration'):
        rc = subprocess.run(["/home/ark/aberration", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart aberration Server
    elif message.content.startswith('$restart aberration'):
        rc = subprocess.run(["/home/ark/aberration", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start ragnarok server
    elif message.content.startswith('$start ragnarok'):
        rc = subprocess.run(["/home/ark/ragnarok", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop ragnarok server
    elif message.content.startswith('$stop ragnarok'):
        rc = subprocess.run(["/home/ark/ragnarok", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart ragnarok Server
    elif message.content.startswith('$restart ragnarok'):
        rc = subprocess.run(["/home/ark/ragnarok", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start scorched earth server
    elif message.content.startswith('$start scorched'):
        rc = subprocess.run(["/home/ark/scorched", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop scorched earth server
    elif message.content.startswith('$stop scorched'):
        rc = subprocess.run(["/home/ark/scorched", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart scorched earth Server
    elif message.content.startswith('$restart scorched'):
        rc = subprocess.run(["/home/ark/scorched", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start the center server
    elif message.content.startswith('$start center'):
        rc = subprocess.run(["/home/ark/center", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop the center server
    elif message.content.startswith('$stop center'):
        rc = subprocess.run(["/home/ark/center", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart the center Server
    elif message.content.startswith('$restart center'):
        rc = subprocess.run(["/home/ark/center", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start crystal isles server
    elif message.content.startswith('$start crystal'):
        rc = subprocess.run(["/home/ark/crystal", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop crystal isles server
    elif message.content.startswith('$stop crystal'):
        rc = subprocess.run(["/home/ark/crystal", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart crystal isles Server
    elif message.content.startswith('$restart crystal'):
        rc = subprocess.run(["/home/ark/crystal", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start extinction server
    elif message.content.startswith('$start extinction'):
        rc = subprocess.run(["/home/ark/extinction", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop extinction server
    elif message.content.startswith('$stop extinction'):
        rc = subprocess.run(["/home/ark/extinction", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart extinction Server
    elif message.content.startswith('$restart extinction'):
        rc = subprocess.run(["/home/ark/extinction", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start valguero server
    elif message.content.startswith('$start valguero'):
        rc = subprocess.run(["/home/ark/valguero", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop valguero server
    elif message.content.startswith('$stop valguero'):
        rc = subprocess.run(["/home/ark/valguero", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart valguero Server
    elif message.content.startswith('$restart valguero'):
        rc = subprocess.run(["/home/ark/valguero", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start genesis server
    elif message.content.startswith('$start genesis'):
        rc = subprocess.run(["/home/ark/genesis", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop genesis server
    elif message.content.startswith('$stop genesis'):
        rc = subprocess.run(["/home/ark/genesis", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart genesis Server
    elif message.content.startswith('$restart genesis'):
        rc = subprocess.run(["/home/ark/genesis", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # start arkadmin server
    elif message.content.startswith('$start arkadmin'):
        rc = subprocess.run(["/home/ark/arkadmin", "start"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # stop arkadmin server
    elif message.content.startswith('$stop arkadmin'):
        rc = subprocess.run(["/home/ark/arkadmin", "stop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # restart arkadmin Server
    elif message.content.startswith('$restart arkadmin'):
        rc = subprocess.run(["/home/ark/arkadmin", "restart"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(rc.stdout)

    # unknown command, return random error message
    else:
        error_quotes = [
            "Krak off, you\'r kiddin\' me!!",
            "C to K error, please remedy",
            "EEP!",
            "Problem exists between Chair and Keyboard. Please examine and remedy, you dumdum",
            "I know not what this is you speak of",
            "Crap!",
            "f*k",
            "Bang! Zoom! Straight to the Moon!"
        ]
        response = random.choice(error_quotes)
        await message.channel.send(response)

    #print(f'{message.author}:::{message.content}')  #echo message to console (debug)

client.run(TOKEN)       #actually start the Discord session
