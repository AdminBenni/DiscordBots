import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
try:
    from BotTokens import *
except ModuleNotFoundError:
    from DiscordBots.BotTokens import *

Client = discord.Client()
client = commands.Bot(command_prefix="")
botName = "TestBot_1#1053"
roles = {
    "admin": "466705244387016714"
}

@client.event
async def on_ready():
    print("bot is ready!")

@client.event
async def on_message(mes):
    print(mes.author, ":", mes.content)
    if mes.content == "lll":
        time.sleep(3)
        await client.send_message(mes.channel, "!bet <@466676207606300697> 2 1")

client.run(bots["testbot2"])