import json
import subprocess
import re
import csv

userdata = [
['DiscordID', 'SteamID'],
['DiscordID2', 'SteamID2']
]

# Function to remove ANSI sequences from strings
def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

rc = subprocess.run("/home/ark/scripts/status.sh", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
reader = csv.DictReader(rc.stdout.decode('ascii').splitlines(),
                        delimiter=' ', skipinitialspace=True,
                        fieldnames = ['slot', 'playername', 'steamid'])


servername = ''
for row in reader:
    slot = row['slot']
    if slot.startswith('**'):
        servername = slot.lstrip("*").rstrip("*")
    else:
        steamid = row['steamid']
        if steamid == kickmesteamid
