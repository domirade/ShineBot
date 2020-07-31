import logging
import random
import asyncio
import discord
from discord import message
from discord.ext import commands
from daily_shadow_mission import daily_async
from datetime import datetime
from enums import Guilds, Users, Roles, CosmeticRoles, Channels
import math
import weather.forecast
import config
import version
import shinebot_token
import timer
    
# standard logging stuff

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
filename = 'shinebottest.log' if config.mode == 'dev' else 'shinebot.log'
handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

__version__ = version.version
mode = config.mode

prefix = '!' 
    # if config.mode == 'dev' 
    # else '%'

# prefix = config.testprefix if config.mode == 'dev' else '%'
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

@bot.command(name='weather')
async def GetForecast(ctx, area: to_lower=None, date: to_lower=None, time: to_lower=None, duration: int=None):
    f""" (Not Implemented) Gets a weather forecast from Mabinogi World Weather API."""
    """Usage: 
    {prefix}weather *<area>*
    {prefix}weather <area> *<day>* 
    {prefix}weather <area> <day> *<duration>*
    
    Examples:
    `%weather rano tomorrow`
    `%weather taillteann today 18:00 6`
    
    If run with no arguments, defaults to a 2-hour forecast of all regions.
    This is the same as running `%weather all now`
    
    Area can be the common name of a map or region, or the numeric regionID used by the game.
    It defaults to 'all' which also enforces a Duration limit of 2 hours to be polite.
    
    Day defaults to 'today' if unspecified which also means 'now' if written in the command.
    It can otherwise accept 'tomorrow' 'yesterday' and any YY-MM-DD format.
    
    Time defaults to the next third-of-an-hour in server time
    
    Duration is the length of the forecast expressed in IRL hours (three 20-minute segments each)
    It's limited to 24 hours for a single area and 2 hours for all of them.
    
    await ctx.send(await weather.forecast.get(area, day, time, duration))
    """
    pass

@bot.command()
async def logout(ctx) -> None:
    """ If this is dev, log out and exit """
    # if config.mode != 'dev':
    #     return
    await ctx.send('Logging out now...')
    await bot.logout()
    bot.close()
    
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
    if ctx.message.author.id == Users['rice']:
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
    bossnames = {
    'boss1': 10,
    'boss2': 22,
    'boss3': 31,
    'boss4': 24
    }
    global boss
    for i, j in bossnames.items():
        if name == i:
            boss = j
        else:
            ctx.send()
    await ctx.send(boss)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"ShineBot Version {__version__}-{mode}")
    channel = bot.get_channel(Channels['Development'])
    if config.mode == 'dev':
        await channel.send('\n'.join((f"{bot.user} reporting for testing!",
                                     f"My version is {__version__}-{mode} and I was run by {config.tester}"
                                     ))
                           )
    else:
        # channel = discord.utils.get(bot.get_all_channels(), guild__name='Shine', name='guild-general')
        await channel.send(f"{bot.user} v{__version__}-{mode} initialized or reconnected.")
        
bot.run(shinebot_token.token)