#!/usr/bin/python3
# bot.py

# Discord Bot for start/stop/update Ark Servers via Discord

# documentation for discord.py is at https://discordpy.readthedocs.io/en/latest/

import discord      # import discord.py library
import subprocess   # import subprocess library
import random       # import random library
from dotenv import load_dotenv      #import function from dotenv library
import asyncio
import json
import csv
import os

# Test for existence of file .env where info like the token for Discord is held
# Do not want to hard code the Discord token here, this file is public on GitHub

# The Discord Token is essentially the bot's login credential for Discord

load_dotenv()
#get Discord token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')
# get id of command channel from .env file
COMMAND_CHANNEL = int(os.getenv('COMMAND_CHANNEL'))
# get id of general channel from .env file
GENERAL_CHANNEL = int(os.getenv('GENERAL_CHANNEL'))
# set intent, new requirement for discord.py version 2.0.0
intents = discord.Intents.default()
intents.message_content = True
# create Discord object
client = discord.Client(intents = intents)


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

# json database for registering kickme command stuff
# check if json file exists
jsonfilename = '/home/ark/scripts/kickme.json'
userdata = {}
if os.path.exists(jsonfilename):
    # Load json file
    with open(jsonfilename) as json_file:
        userdata = json.load(json_file)

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
"genesis2",
"arkadmin",
"arkserver",
"lostisland",
"fjordur",
"epicisland"
]

# Test for valid server name
def isvalidserver(servername):
    # iterate through server list
    for validserver in serverlist:
        # if valid server name is found, return True
        if servername == validserver:
            return True
    # if no valid name found, return False
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
#        "Problem exists between Chair and Keyboard. Please examine and remedy, you dumdum",
        "I know not what this is you speak of",
        "Crap!",
        "f*k",
        "Bang! Zoom! Straight to the Moon!",
        "Your keyboard must be upside down",
        "He's dead Jim",
        "I canna' do it cap'm, we need more pow'a",
        "I cannot tell a lie.  You, sir, need to. fuck. off.",
        "All your base are belong to me",
        "Hello. My name is Inigo Montoya. You killed my father. Prepare to die.",
        "Bad monkey, no juicebox for you!",
        "Perhaps you could do better if I got you a BahNahNah",
        "Hey Joe, when you're done showering, maybe we could get some work done",
        "Nope",
        "Try Again",
        "Dangit!",
        "Get it together you overgrown beer can!",
        "~~Sigh",
        "bummer"
    ]
    await message.channel.send(random.choice(error_quotes))
    return

# Function to remove ANSI sequences from strings
import re
def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

# Write data to json file for non volatile storage
def writejson(data):
    with open(jsonfilename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Function to check if any players are connected to any instances
# Returns dict of server names sorted by vacant or occupied
def anybodyhome():
    # get server status
    rc = subprocess.run("/home/ark/scripts/status.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    reader = csv.DictReader(rc.stdout.splitlines(), delimiter=',', skipinitialspace=True, fieldnames = ['playername', 'steamid'])
    #initialize tracking variables
    servers = { "init": "value", }
    servers['vacant'] = set(())
    servers['occupied'] = set(())
    servername = ''
    # scan returned status data
    for row in reader:
        name = str(row['playername'])
        if name.startswith('**'):
            # parse servername, since they start and end with '**'
            servername = name.lstrip("*").rstrip("*")
        elif ((name == "No Players Connected ") or (name == "Connection failed.") or (name == "Error 111: Connection refused") or (name == "")):
            # check for no players connected, add server to vacant set
            servers['vacant'].add(servername)
        else:
            # otherwise, assume playername is listed, add server to occupied set
            servers['occupied'].add(servername)
    return servers

# Function to start set of Servers
async def startservers(args, message):
    # loop through provided servernames
    for item in args:
        # check if servername is valid
        if isvalidserver(item):
            await runprocesstodiscord(
                "/home/ark/" + item + " start",
                "__**:Starting " + item + ":**__\n",
                message)
        else:
            # Report invalid servername
            await message.channel.send("__**>>Bad Server Name: " + item + "<<**__")

# Function to stop set of servers
async def stopservers(args, message):
    # loop through provided servernames
    for item in args:
        if isvalidserver(item):
            await runprocesstodiscord(
                ["/home/ark/" + item + " stop"],
                "__**:Stopping " + item + ":**__\n",
                message)
        else:
            # report invalid servername
            await message.channel.send("__**>>Bad Server Name: " + item + "<<**__")

# when Discord session is ready, echo status to console
@client.event
async def on_ready():
    print(
        f'{client.user} has connected to Discord!\n'
        f'{client.user} is connected to the following guild:\n'
)
    # list channels we are linked to
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})\n')

# when a message is received in the channel
@client.event
async def on_message(message):
    #ignore messages from myself
    if message.author == client.user:
        return

    # ignore messages not starting with commandchar
    if not(message.content.startswith(commandchar)):
        return

    # equivalent to hello world
    if message.content.startswith(commandchar + 'hello'):
        # command channel check
#        if message.guild.id != COMMAND_CHANNEL: return
        await message.channel.send('What\'s Krackin\'?')

    # help command. Shows different help message depending on which
    # channel the command came from
    elif message.content.startswith(commandchar + 'help'):
        # command channel check
        if message.guild.id == COMMAND_CHANNEL:
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

**$check**
checks if an update is available

**$force** -
invokes LGSM forced update. All running servers are given 10 minute notification, stopped, updated, and restarted.
*Cheat mode*: if you invoke $force when no players are connected, servers are stopped and restarted automatically and the 10 minute notification is bypassed.

**$backup** -
invokes LGSM backup. All running servers are given 10 minute notification, stopped, backedup, updated, and restarted. Same cheat as $force

**$destroywilddinos <server> [<server2> <server3> ...]** -
sends destroywilddinos to listed <server> consoles.  All wild dinos are removed from the map. Does not affect tamed dinos.

**$kick <server> <playersteamid>** -
sends kick command to <server> to kick <playersteamid>, the numeric identifier supplied after player name in $status

**$kickme**
sends kick command to whatever server you are connected to. you must register your steamid with $kickmeregister

**$kickmeregister <steamid>**
registers your <steamid> to Ark Server Bot so $kickme works.
YOU CAN ONLY DO THIS ONCE
to change your registered <steamid>, ping the bot man (StinkyMcKraken)

**Use $% to show servers list**
"""
        else:
            helpmessage = """__**Ark Server Bot Commands:**__
**$help** -
this message

**$status** -
lists all running servers and players connected

**$check**
checks for avaliable update

**$kickme**
sends kick command to whatever server(s) you are connected to. you must register your steamid with $kickmeregister. steamid visible in $status when connected to ark cluster

**$kickmeregister <steamid>**
registers your <steamid> to Ark Server Bot so $kickme works.
YOU CAN ONLY DO THIS ONCE
to change your registered <steamid>, ping the bot man (StinkyMcKraken)

Server information is pinned to this channel and is updated as needed.
Click the pushpin icon and scroll to the bottom of the pins list to find instructions for connecting to our servers.
"""
        await message.channel.send(helpmessage)

    elif message.content.startswith('$%'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
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
27010 genesis2
27011 arkadmin (island)
27012 lostisland
27013 fjordur
27014 epicisland (no mods)
"""
        await message.channel.send(helpmessage)

    # bot server status
    elif message.content.startswith(commandchar + 'status'):
        rc = subprocess.run("/home/ark/scripts/status.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await message.channel.send(escape_ansi(rc.stdout))

    # LGSM Check for update
    elif message.content.startswith(commandchar + 'check'):
        # run command
        await runprocesstodiscord(
            "/home/ark/arkserver check-update",
            "bot.py: Checking for Update...\n",
            message)

    # ark force update
    elif message.content.startswith(commandchar + 'force'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
        # check if any servers are occupied
        servers = anybodyhome()
        if (len(servers['occupied']) == 0):
            # if no occupied servers, stop all servers
            await message.channel.send("**No Players Connected to servers**")
            await stopservers(servers['vacant'], message)
            # run force update command script
            await runprocesstodiscord(
                "/home/ark/scripts/multipleupdate.sh",
                "Starting Forced Update. Please wait 5-8 minutes for update to complete.\n",
                message)
            # restart servers that were stopped
            await startservers(servers['vacant'], message)
        else:
            # else some servers are occupied, let the script send notifications
            # run command
            await runprocesstodiscord(
                "/home/ark/scripts/multipleupdate.sh",
                "Starting Forced Update in-game notification script. Please wait 15 minutes for update and restart to complete.\n",
                message)
        await message.channel.send("__**bot.py: Update and Restart complete.**__")

    # ark backup
    elif message.content.startswith(commandchar + 'backup'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
        # check if any servers are occupied
        servers = anybodyhome()
        if (len(servers['occupied']) == 0):
            # if no occupied servers, stop all servers
            await message.channel.send("**No Players Connected to servers**")
            await stopservers(servers['vacant'], message)
            # run force update command script
            await runprocesstodiscord(
                "/home/ark/scripts/multiplebackup.sh",
                "Starting Forced Update. Please wait 25 minutes for backup to complete.\nServers will be restarted automatically.\n",
                message)
            # restart servers that were stopped
            await startservers(servers['vacant'], message)
        else:
            # else some servers are occupied, let the script send notifications
            # run command
            await runprocesstodiscord(
                "/home/ark/scripts/multiplebackup.sh",
                "Starting Backup in-game notification script. Please wait 30-40 minutes for backup, update, and restart to complete.\n",
                message)
        await message.channel.send("__**bot.py: Backup, Update, and Restart complete.**__")

    # kickmeregister command, one argument, steamid
    # this command must be listed before kickme and kick
    # because otherwise it will trigger those commands first
    elif message.content.startswith(commandchar + 'kickmeregister'):
        # parse arguments
        userid = str(message.author.id)
        username = str(message.author.name)
        args = message.content.split(" ")
        # remove first item, the command itself
        args.pop(0)
        # check author against database
        try:
            steamid = userdata[userid]['steamid']
        # if author not in database
        except KeyError:
            # if no argument
            if len(args) == 0:
                # display usage
                await message.channel.send("You are not registered. Use " + commandchar + "kickmeregister <SteamID> to register yourself in " + commandchar + "kickme. Your <steamid> is the number listed after your name in " + commandchar + "status")
                return
            # if argument, check to see if steamid is already registered
            for player in userdata:
                if args[0] == userdata[player]['steamid']:
                    await message.channel.send("SteamID " + args[0] + " already registered to " + userdata[player]['name'])
                    return
            # add user to database
            userdata[userid] = {
                'steamid' : args[0],
                'name' : username  # including Discord Username so I can manually delete people out of the json file
            }
            # save database to json file
            writejson(userdata)
            # report add
            await message.channel.send(commandchar + "kickme registered " + userdata[userid]['name'] + " as " + userdata[userid]['steamid'])
            return
        await message.channel.send("You are already registered as " + userdata[userid]['steamid'] + ".  To change or remove your registration, ping the bot man (StinkyMcKraken)")

    # kickme command, no arguments
    # this command must be listed before kick
    # because otherwise it will trigger kick first
    elif message.content.startswith(commandchar + 'kickme'):
        # check author against database
        try:
            kickmesteamid = str(userdata[str(message.author.id)]['steamid'])
        except KeyError:
            # if author not in database, respond with kickmeregister usage
            await message.channel.send("You are not registered. Use " + commandchar + "kickmeregister <SteamID> to register yourself in " + commandchar + "kickme")
            return
        # get server status
        rc = subprocess.run("/home/ark/scripts/status.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        reader = csv.DictReader(rc.stdout.splitlines(), delimiter=',', skipinitialspace=True, fieldnames = ['playername', 'steamid'])
        # find out which server user is on
        kickservers = []
        servername = ''
        for row in reader:
            name = str(row['playername'])
            if name.startswith('**'):
                # parse servername, since they start and end with '**'
                servername = name.lstrip("*").rstrip("*")
            else:
                # locate steamid in the list
                steamid = str(row['steamid']).lstrip(" ").rstrip(" ")
                if (steamid == kickmesteamid):
                    # add servername to list of servers where kicking should ensue
                    kickservers.append(servername)
                    # capture playername. using split() to separate out the leading number
                    playernametodisplay = name.split('.')[1]
        if (servername == ''):
            # if no servers running, report as such
            await message.channel.send("No Servers Running")
        else:
            # send kick command to relevant server(s)
            returnmessage = ''
            for server in kickservers:
                returnmessage = returnmessage + "Kicking" + playernametodisplay + " from " + server + "\n"
                rc = subprocess.run(["/home/ark/rcon", server, "KickPlayer " + kickmesteamid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            # if player not found change the message
            if returnmessage == '':
                returnmessage = "Player not found on any servers"
            await message.channel.send(returnmessage)

    # send kick command to given instance
    # usage: %kick <server> <playerID>
    elif message.content.startswith(commandchar + 'kick'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
        # parse arguments
        args = message.content.split(" ")
        # test if $kick command was supplied with two arguments
        if len(args) == 3:
            rc = subprocess.run(["/home/ark/rcon", args[1], "KickPlayer " + args[2]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            await message.channel.send(escape_ansi(rc.stdout))
        else:
            await message.channel.send("Usage: " + commandchar + "kick <server> <playersteamid>")

    # ark update lgsm
    elif message.content.startswith(commandchar + 'update lgsm'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
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

    # start <server> [<server> <server> ...]
    elif message.content.startswith(commandchar + 'start'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
        # separate arguments into a list
        args = message.content.split(" ")
        # remove first item in list, it is the command given
        args.pop(0)
        # test if command was supplied with at least one argument
        if len(args) >= 1:
            await startservers(args, message)
        else:
            await returninsult(message)

    # stop <server> [<server> <server> ...]
    elif message.content.startswith(commandchar + 'stop'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
        # separate arguments into a list
        args = message.content.split(" ")
        # remove first item in list, it is the command given
        args.pop(0)
        # test if command was supplied with at least one argument
        if len(args) >= 1:
            # handoff to function used by other commands
            await stopservers(args, message)
        else:
            # Report invalid syntax
            await returninsult(message)

    # restart <server> [<server> <server> ...]
    elif message.content.startswith(commandchar + 'restart'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
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

    # send destroywilddinos to given servername
    elif message.content.startswith(commandchar + 'destroywilddinos'):
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
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
                        ["/home/ark/rcon " + item + " destroywilddinos"],
                        "__**:Destroying Wild Dinos on " + item + ":**__\n",
                        message)
                else:
                    # error message
                        await message.channel.send("__**>>Bad Server Name: " + item + "<<**__")
        else:
            await returninsult(message)

    # unknown command, return random error message
    else:
        # command channel check
        if message.guild.id != COMMAND_CHANNEL: return
        await returninsult(message)



# actually start the Discord session
client.run(TOKEN)
