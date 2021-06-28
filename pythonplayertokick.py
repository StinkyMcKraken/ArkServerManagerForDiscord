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

"""

kickmesteamid = '76561198393377424'

reader = csv.DictReader(data.splitlines(), delimiter=',', skipinitialspace=True, fieldnames = ['playername', 'steamid'])

kickservers = []
servername = ''
for row in reader:
    name = row['playername']
    if name.startswith('**'):
        # parse servername, since they start and end with '**'
        servername = name.lstrip("*").rstrip("*")
        print(servername)
    else:
        # locate steamid in the list
        steamid = row['steamid']
        if (str(steamid) == str(kickmesteamid)):
            # add servername to list of servers where kicking should ensue
            kickservers.append(servername)
            # capture playername. using split() to separate out the leading number
            playernametodisplay = name.split('.')[1]

for server in kickservers:
    print('Kicking' + str(playernametodisplay) + ' from ' + server)
