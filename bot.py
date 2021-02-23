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

# Initialize constants

# Initialize command character
commandchar = "$"

# Initialize list of valid servers
serverlist = [
"island",
"aberration",
"ragnarok",
"scorched",
"center",
"crystal",
"extinction",
"valguero",
"genesis",
"arkadmin"
]

# Test for valid server name
def isvalidserver(servername):
    #iterate through server list
    for validserver in serverlist:
        #if valid server name is found, return True
        if servername == validserver:
            return True
    #if no valid name found, return False
    return False

# Runs given command and feeds it's stdout to Discord in realish time
async def runprocesstodiscord(cmd, output, message):
    rcmessage = await message.channel.send(output)
    rc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Poll process for new output until finished
    while True:
        nextline = rc.stdout.readline()
        if nextline == '' and rc.poll() is not None:
            break
        #print(f'{nextline}')  #echo message to console (debug)
        output = output + escape_ansi(nextline)
        if len(output) > 2000:
            output = nextline
            rcmessage = await message.channel.send(output)
        else:
            await rcmessage.edit(content=output)
    return

# Error message generator
async def returninsult(message):
    error_quotes = [
        "Krak off, you\'r kiddin\' me!!",
        "C to K error, please remedy",
        "EEP!",
        "Problem exists between Chair and Keyboard. Please examine and remedy, you dumdum",
        "I know not what this is you speak of",
        "Crap!",
        "f*k",
        "Bang! Zoom! Straight to the Moon!",
        "Your keyboard must be upside down"
    ]
    await message.channel.send(random.choice(error_quotes))
    return

# Function to remove ANSI sequences from strings
import re
def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

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

    if not(message.content.startswith(commandchar)):  # ignore messages not starting with commandchar
        return

    # equivalent to hello world
    if message.content.startswith(commandchar + 'hello'):
        await message.channel.send('What\'s Krackin\'?')

    # help command
    elif message.content.startswith(commandchar + 'help'):
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

**$start <server> [<server2> <server3> ...]** -
this is known

**$stop <server> [<server2> <server3> ...]** -
Instant stop, no check for connected players

**$restart <server> [<server2> <server3> ...]** -
stops then starts <server>. Instant stop, no check for players

**$force update** -
invokes LGSM forced update. All running servers are given 10 minute notification, stopped, updated, and restarted.
*Cheat mode*: if you manually stop all running servers prior to running this command, it will skip the 10 minute notification process. Servers will need to be manually restarted after the update.

**$backup** -
invokes LGSM backup. All running servers are given 10 minute notification, stopped, backedup, updated, and restarted. Same cheat as $force update

**$update lgsm** -
updates LGSM itself on all instances. Should not be necessary but may be needed if other commands fail. Does not stop servers

**$kick <server> <playersteamid>** -
sends kick command to <server> to kick <playersteamid>, the numeric identifier supplied after player name in $status

**Use $% to show servers list**
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
    elif message.content.startswith(commandchar + 'status'):
        rc = subprocess.run("/home/ark/scripts/status.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(escape_ansi(rc.stdout))

    # ark force update
    elif message.content.startswith(commandchar + 'force update'):
        await runprocesstodiscord(
            "/home/ark/scripts/multipleupdate.sh",
            "Starting Forced Update in-game notification script. Please wait 15 minutes for update and restart to complete.\n",
            message)
        await message.channel.send("__**Update and Restart complete.**__")

    # ark backup
    elif message.content.startswith(commandchar + 'backup'):
        await runprocesstodiscord(
            "/home/ark/scripts/multiplebackup.sh",
            "Starting Backup in-game notification script. Please wait 30-40 minutes for backup, update, and restart to complete.\n",
            message)
        await message.channel.send("__**Backup, Update, and Restart complete.**__")

    # send kick command to given instance
    # usage: %kick <server> <playerID>
    elif message.content.startswith(commandchar + 'kick'):
        args = message.content.split(" ")
        # test if command was supplied with two arguments
        if len(args) == 3:
            rc = subprocess.run(["/home/ark/rcon", args[1], "KickPlayer " + args[2]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            await message.channel.send(escape_ansi(rc.stdout))
        else:
            await message.channel.send("Usage: " + commandchar + "kick <server> <playersteamid>")

    # ark update lgsm
    elif message.content.startswith(commandchar + 'update lgsm'):
        # run update lgsm on generic instance
        await runprocesstodiscord(
            "/home/ark/arkserver ul",
            "__**:Updating LGSM:**__\n",
            message)
        # copy generic instance main script to other scripts
        for instance in serverlist:
            rc = subprocess.run(["cp", "/home/ark/arkserver", "/home/ark/" + instance])
        # done
        await message.channel.send("**:LGSM updated on all instances:**")

    # start <server>
    elif message.content.startswith(commandchar + 'start'):
        # separate arguments into a list
        args = message.content.split(" ")
        # remove first item in list, it is the command given
        args.pop(0)
        # test if command was supplied with at least one argument
        if len(args) >= 1:
            # loop through provided servernames
            for item in args:
                if isvalidserver(item):
                    await runprocesstodiscord(
                        "/home/ark/" + item + " start",
                        "__**:Starting " + item + ":**__\n",
                        message)
                else:
                    await message.channel.send("__**>>Bad Server Name: " + item + "<<**__")
        else:
            await returninsult(message)

    # stop <server>
    elif message.content.startswith(commandchar + 'stop'):
        # separate arguments into a list
        args = message.content.split(" ")
        # remove first item in list, it is the command given
        args.pop(0)
        # test if command was supplied with at least one argument
        if len(args) >= 1:
            # loop through provided servernames
            for item in args:
                if isvalidserver(item):
                    await runprocesstodiscord(
                        ["/home/ark/" + item + " stop"],
                        "__**:Stopping " + item + ":**__\n",
                        message)
                else:
                    await message.channel.send("__**>>Bad Server Name: " + item + "<<**__")
        else:
            await returninsult(message)

    # restart <server>
    elif message.content.startswith(commandchar + 'restart'):
        # separate arguments into a list
        args = message.content.split(" ")
        # remove first item in list, it is the command given
        args.pop(0)
        # test if command was supplied with at least one argument
        if len(args) >= 1:
            # loop through provided servernames
            for item in args:
                if isvalidserver(item):
                    await runprocesstodiscord(
                        ["/home/ark/" + item + " restart"],
                        "__**:Restarting " + item + ":**__\n",
                        message)
                else:
                    # error message
                    await message.channel.send("__**>>Bad Server Name: " + item + "<<**__")
        else:
            await returninsult(message)

    # unknown command, return random error message
    else:
        await returninsult(message)

    #print(f'{message.author}:::{message.content}')  #echo message to console (debug)

client.run(TOKEN)       #actually start the Discord session
