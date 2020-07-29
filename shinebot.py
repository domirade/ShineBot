import config
import logging
import random
from discord.ext import commands
from daily_shadow_mission import daily_async
from discord.ext import commands
import authtoken
import weather.forecast

# standard logging stuff

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
filename = 'shinebottest.log' if config.mode == 'dev' else 'shinebot.log'
handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

version = config.version
mode = config.mode

# initialize command prefix based on the mode

prefix = config.testprefix if config.mode == 'dev' else '%'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   case_insensitive=True)

def to_lower (arg):
    return arg.lower()

# commands

@bot.command(name='ping')    
async def heartbeat(ctx) -> str:
    """ Asks the bot for a response.
    "Hello? Are you still there?" """
    response = 'pong\n'
    if config.mode == 'dev':
        response += f"Latency {math.trunc(bot.latency*1000)}ms\n"
        response += f'This instance run by {config.tester}'
    await ctx.send(response)
        
@bot.command(name='daily')
async def DailyShadowMission(ctx, *args):
    """ args will be parsed in func `daily()` """
    response = await daily_async.daily(*args)
    await ctx.send(response)

@bot.command(name='weather')
async def GetForecast(ctx, area: to_lower=None, date: to_lower=None, time: to_lower=None, duration: int=None) -> str:
    """ Gets a weather forecast from Mabinogi World Weather API.
    
    Usage: 
    %weather *<area>*
    %weather <area> *<day>* 
    %weather <area> <day> *<duration>*
    
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
    if config.mode != 'dev':
        return
    await ctx.send('りょうかいしました')
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
    if ctx.message.author.id == 192862829362020352:
        response += 'You are: 101% Smelly! Oh god it\'s like a diaper filled with Indian food...'
    else:
        response += f'You are: {random.randint(0,100)}% Smelly! ' + random.choice(_quips)
    await ctx.send(response)

# finish initialization

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"ShineBot Version {version}-{mode}")
    if config.mode == 'dev':
        channel = discord.utils.get(bot.get_all_channels(), guild__name='Shine', name='shinebot-dev')
        await channel.send('\n'.join((f"{bot.user} reporting for testing!",
                                     f"My version is {version}-{mode} and I was run by {config.tester}"
                                     ))
                           )
    else:
        channel = discord.utils.get(bot.get_all_channels(), guild__name='Shine', name='guild-general')
        await channel.send(f"{bot.user} v{version}-{mode} initialized or reconnected.")

bot.run(authtoken.token)