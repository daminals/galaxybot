# bot.py
# Daniel Kogan Taseen Islam Aritro Sarkar
# 01.28.2022

import discord, os, json, random, requests
import wikipedia
import barter
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get('TOKEN', 3)

from discord.ext import commands
bot = commands.Bot(command_prefix=">")
g_rarity = []    

class GALAXY_OBJECT:
    def __init__(self, gdict):
        self.name = gdict["name"]
        self.rarity = gdict["rarity"]
        self.wikipedia = gdict["wikipedia"]
        self.wname = gdict['wname']
        self.points = int((1/self.rarity) * 1000)
        self.img = gdict["main_img"]

        for i in range(self.rarity):
            g_rarity.append(self)

    def shorten(self, summary):
        summary = summary.split("\n")[0]
        return summary

    def embed(self, user):
        display = discord.Embed(title=self.name, description=self.shorten(wikipedia.summary(self.wname)), colour=0x87CEEB)
        #display.set_author(name="galaxybot", icon_url=self.img)
        display.set_image(url=self.img)
        display.add_field(name="User", value=user, inline=False)
        display.add_field(name="Points", value=self.points, inline=False)
        return display

with open('galaxy.json', 'r+') as galaxyjson:
    galaxies = json.load(galaxyjson)

for i in galaxies:
    GALAXY_OBJECT(galaxies[i])

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def galaxy(ctx):
    chosen = random.choice(g_rarity)
    await ctx.send(embed=chosen.embed(ctx.author))
    barter.add_points(str(ctx.author.id), chosen.points)
    #print(g_rarity)
    

bot.run(TOKEN)