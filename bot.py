# bot.py
import os

import discord
import subprocess
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(
        f'{client.user} has connected to Discord!\n'
        f'{client.user} is connected to the following guild:\n'
)
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})\n')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #equivalent to hello world
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #create a test file
    elif message.content.startswith('$touch'):
        rc = subprocess.call("/home/ark/discordbot/touch.sh")
        await message.channel.send(rc)

    #start ark server command
    elif message.content.startswith('$ark start'):
        rc = subprocess.call("/home/ark/arkserver", "start")

    #stop ark server command
    elif message.content.startswith('$ark stop'):
        rc = subprocess.call("/home/ark/arkserver", "stop")

    #ark server update
    elif message.content.startswith('$ark update'):
        rc = subprocess.call("/home/ark/arkserver", "update")

    #ark force update
    elif message.content.startswith('$ark force update'):
        rc = subprocess.call("/home/ark/arkserver", "fu")

    #ark update lgsm
    elif message.content.startswith('$ark update lgsm'):
        rc = subprocess.call("/home/ark/arkserver", "update-lgsm")

    print(f'{message.author}:::{message.content}')

client.run(TOKEN)
