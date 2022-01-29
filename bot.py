# bot.py
# Daniel Kogan Taseen Islam Aritro Sarkar
# 01.28.2022

import discord, os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get('TOKEN', 3)

bot = discord.Bot()
from discord.ext import commands

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot = commands.Bot(command_prefix=">")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

bot.run(TOKEN)
