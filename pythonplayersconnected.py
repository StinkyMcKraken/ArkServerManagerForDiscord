import csv

# https://www.w3schools.com/python/trypython.asp?filename=demo_default

data = """**aberration**

0. Clockwork_Kitten, 76561198898721578
1. Rogue Kraken, 76561198393377424
2. Snipergrrl, 76561198144879686

**arkadmin**

0. mbalch13, 76561197990379506
1. EvlGngr, 76561198817399316
2. Rogue Kraken, 76561198393377424

**center**
No Players Connected

**genesis2**
Connection failed.
Error 111: Connection refused

"""

kickmesteamid = '76561198393377424'

reader = csv.DictReader(data.splitlines(), delimiter=',', skipinitialspace=True, fieldnames = ['playername', 'steamid'])

# print playername
#print('PlayerName')
#for row in reader:
#    print("PN: " + str(row['playername']) + " SID: " + str(row['steamid']))

# print steamid ## Note, can only iterate through reader once, which is why i had to display steamid above
#print('\nSteamID')
#for row in reader:
#    print(row['steamid'])

#initialize tracking variables
vacant = set(())
occupied = set(())
servername = ''
for row in reader:
    print("PN: " + str(row['playername']) + " SID: " + str(row['steamid']))
    name = row['playername']
    if name.startswith('**'):
        # parse servername, since they start and end with '**'
        servername = name.lstrip("*").rstrip("*")
        print(servername)
    elif ((name == "No Players Connected") or (name == "Connection failed.") or (name == "Error 111: Connection refused")):
        # check for no players connected, add server to vacant set
        vacant.add(servername)
    else:
        # otherwise, assume playername is listed, add server to occupied set
        occupied.add(servername)

print("\nLength of Occupied: " + str(len(occupied)))

print('\nLength of Vacant: ' + str(len(vacant)))
