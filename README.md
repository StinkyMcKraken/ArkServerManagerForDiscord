# ArkServerManagerForDiscord
Allow players to start, stop, or update ARK:Survival Evolved servers via Discord on a dedicated host without needing shell access to the host. This project interfaces with Discord, LinuxGSM and a few Bash scripts I wrote to handle automatic server shutdowns, backups, and updates.  My intent is to allow players to start, stop, and force update servers as needed.  

One issue we keep having is the developer of ARK:Survival Evolved will push client and server updates at varied times of day, however my servers only check for updates once per day.  When an update happens mid-day, frequently players cannot join the server until it auto updates at 6am or admin intervenes.  I would like players to be able to request the server update without admin intervention.

We have about 4-6 players on our servers.  Each server is running a different map.  Players typically spend time focused on one map.  Every few months, they switch to a different map.  Tamed creatures on untended servers will die off because Ark continues running its simulation even with no players.  If one or more players want to hop to a map that is not running, it currently requires admin intervention.  I wish to allow players to start and stop servers on their own.

Stopping servers runs a check via RCON to make sure no players are connected before the server is stopped to prevent trolling.  This feature could be expanded to automatically stop a server if no players have connected in a certain period of time.
