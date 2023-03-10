from utils import getConfigFromFile

import discord
import asyncio
import requests
import os

from discord.ext import commands
from discord.ext.commands import Greedy, Context

from typing import Literal, Optional

CONFIG = getConfigFromFile()
TOKEN = CONFIG['test_bot_token']
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, application_id='1078657655473709087')

@bot.event
async def on_ready():
    print('Online')

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    # loads cogs before starting
    await load()
    await bot.start(TOKEN)

asyncio.run(main())