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
        await client.send_message(mes.channel, "!startbet Option One, Option Two")
    elif mes.content == "lll2":
        await client.send_message(mes.channel, "!endbet 1")

client.run(bots["testbot"])