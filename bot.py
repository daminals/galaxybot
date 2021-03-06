# bot.py
# Daniel Kogan Taseen Islam Aritro Sarkar
# 01.28.2022

from discord.ext import commands
from dotenv import load_dotenv
import barter
import wikipedia
import discord
import os
import json
import random
import requests
import asyncio
intents = discord.Intents.all()
load_dotenv()
TOKEN = os.environ.get('TOKEN', 3)

bot = commands.Bot(command_prefix=">", intents=intents)


class GALAXY_OBJECT:
    def __init__(self, gdict):
        self.name = gdict["name"]
        self.stable_rarity = gdict["rarity"]
        self.rarity = gdict["rarity"]
        self.wikipedia = gdict["wikipedia"]
        self.wname = gdict['wname']
        self.points = int((1/self.rarity) * 1000)
        self.img = gdict["main_img"]

    def shorten(self, summary):
        summary = summary.split("\n")[0]
        return summary

    def embed(self, user):
        display = discord.Embed(title=self.name, description=self.shorten(
            wikipedia.summary(self.wname)), colour=0x87CEEB)
        #display.set_author(name="galaxybot", icon_url=self.img)
        display.set_image(url=self.img)
        display.add_field(name="User", value=user, inline=False)
        display.add_field(
            name="Rarity", value=self.stable_rarity, inline=False)
        display.add_field(name="Points", value=self.points, inline=False)
        return display


with open('galaxy.json', 'r+') as galaxyjson:
    galaxies = json.load(galaxyjson)


# leaderboard function for any desired datapoint
async def leaderboard(ctx, individual, datapoint):
    leaderboard = "```"
    data = barter.readJSON("user.json")
    if individual:
        count = data[str(individual.id)][datapoint]
        lname = str(individual.name) + '#' + \
            str(individual.discriminator) + ':' + str(count) + '\n'
        ud = await ctx.send(leaderboard + lname + '```')
        return
    server = ctx.guild
    leaderboard_no_format = []
    for user in data:
        discord_user = bot.get_user(int(user))
        if discord_user in server.members:
            count = data[user][datapoint]
            lname = str(discord_user.name) + '#' + \
                str(discord_user.discriminator) + ': ' + str(count) + '\n'
            leaderboard_no_format.append([count, lname])
    leaderboard_no_format = sorted(leaderboard_no_format)
    leaderboard_no_format = leaderboard_no_format[::-1]
    leaderboard = "```"
    for i in leaderboard_no_format:
        leaderboard += i[1]
    ud = await ctx.send(leaderboard + '```')
    """
    message = ud.content
    start = 1
    for i in range(10000000):
        message = message.split('\n')
        start *= 2
        for index, i in enumerate(message):
            if 'maccabee' in i:
                j = i.split(' ')
                j[1] = " " + str(int(j[1]) + start)
                message[index] = "".join(j)
        message = "\n".join(message)
        await ud.edit(content=message)
        await asyncio.sleep(1)
    """


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command()  # show off points
async def points(ctx, individual: discord.Member = None):
    await leaderboard(ctx, individual, "points")


@bot.command()  # show off charms
async def charms(ctx, individual: discord.Member = None):
    await leaderboard(ctx, individual, "charms")


@bot.command()
async def shop(ctx):
    embed = discord.Embed(
        title="Shop", description="Galaxy Shop. Use >buy item_name to purchase items with your points! Enter 'basic', 'super', or 'galatic' to purchase your charm!", colour=0x87CEEB)
    embed.add_field(name="Basic Charm",
                    value="500 points, makes rarer galaxies appear more frequently for you!", inline=False)
    embed.add_field(name="Super Charm",
                    value="2000 points, 5 times more effective than basic charm!", inline=False)
    embed.add_field(name="Galatic Charm",
                    value="5000 points, 3 times more effective than the Super Charm!", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def buy(ctx, charm):
    if charm.lower() in barter.shop:
        await ctx.send(barter.add_charm(str(ctx.author.id), charm))
    else:
        await ctx.send("that charm doesn't seem to be in the shop.")


@bot.command()
async def missing(ctx):
    all = barter.readJSON('galaxy.json')
    user_disc = []
    missing = []
    missing_string = '```'
    for i in barter.readJSON('user.json')[str(ctx.author.id)]['discovered']:
        user_disc.append(i)
    for i in all:
        if all[i]['name'] not in user_disc:
            missing.append(all[i]['name'])
            missing_string += all[i]['name'] + '\n'
    await ctx.send(missing_string + '```')


@bot.command()
async def galaxy(ctx):
    # initialize
    g_rarity = []
    charm = 0
    try:
        data = barter.readJSON("user.json")[str(ctx.author.id)]
        charm = data["charms"]
    except:
        print('new user')
    # create a weighted list of galaxies
    for i in galaxies:
        galaxy_obj = GALAXY_OBJECT(galaxies[i])
        if galaxy_obj.rarity < 44:
            galaxy_obj.rarity += charm
        for i in range(galaxy_obj.rarity):
            g_rarity.append(galaxy_obj)
    # randomly choose from generated list
    chosen = random.choice(g_rarity)
    await ctx.send(embed=chosen.embed(ctx.author))
    barter.add_points(str(ctx.author.id), chosen.points, chosen.name)
    try:
        data = barter.readJSON("user.json")[str(ctx.author.id)]
        if len(data['discovered']) >= 25:
            await ctx.send("Congrats! You have discovered every galaxy!", file=discord.File('winner.png'))
    except:
        print('new user')


bot.run(TOKEN)
