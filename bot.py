# bot.py
# Daniel Kogan Taseen Islam Aritro Sarkar
# 01.28.2022

import discord

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")

bot.run("your token here")
