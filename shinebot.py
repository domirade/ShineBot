import config
import logging
import shinebot_token
import math
import random
import asyncio
import discord
from discord import message
from discord.ext import commands
from daily_shadow_mission import daily_async
from datetime import datetime
import timer


# standard logging stuff
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='shinebot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# initialize command prefix based on the mode

prefix = '!' 
    # if config.mode == 'dev' 
    # else '%'

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   case_insensitive=True)
# commands

@bot.command(name='ping')
async def heartbeat(ctx):
    """ Check if the bot's alive """
    response = 'PONG!\n'
    # if config.mode == 'dev':
        # response += str(bot.latency)
    await ctx.send(response)
        
@bot.command(name='daily')
async def DailyShadowMission(ctx, *args):
    """ args will be parsed in func `daily()` """
    response = await daily_async.daily(*args)
    await ctx.send(response)

@bot.command()
async def logout(ctx):
    """ If this is dev, log out and exit """
    # if config.mode != 'dev':
    #     return
    await ctx.send('Logging out now...')
    await bot.logout()
    
@bot.command()
async def rice(ctx):
    """ bully people, I guess """
    response = ctx.message.author.mention + ' '
    _quips = ['8^y',
              'How about that?',
              'Huh.',
              'Interesting...',
              'LOL!',
              'The More You Know:tm:',
              '<:awesome:720802781488742410>']
    if ctx.message.author.id == 192862829362020352:
        response += 'You are: 101% Smelly! Oh god it\'s like a diaper filled with Indian food...'
    else:
        response += f'You are: {random.randint(0,100)}% Smelly! ' + random.choice(_quips)
    await ctx.send(response)

@bot.command(name='timer')
async def time1(ctx, name):
    now = datetime.now()
    # for i in range(len(bossname)):
    #     if bossname[i] == name
    #         y = bossname[i]
    #     else
    current_time = now.strftime("%H:%M:%S") + " " + "Reminder in "+ str(name) + " hours"
    await ctx.send(current_time)

@bot.command(name='boss')
async def boss(ctx, name):
    # for i in range(len(bossnames[i])):
    #     if bossnames[i] == name:
    #         y = bossnames[i]
    #     else:
    #         pass
    await ctx.send(bossnames[1])

# finish initialization

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print('ShineBot version {0.version} build {0.build}'.format(config))

bot.run(shinebot_token.token)
