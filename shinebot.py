import logging
import random
import discord
from enums import Guilds, Users, Roles, CosmeticRoles, Channels
from discord.ext import commands
from daily_shadow_mission import daily_async
import math
import weather.forecast
import config
import version
from authtoken import token

    
# standard logging stuff

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
filename = 'shinebottest.log' if config.mode == 'dev' else 'shinebot.log'
handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

mode = config.mode

# initialize command prefix based on the mode

prefix = config.testprefix if config.mode == 'dev' else '%'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   case_insensitive=True)

# helper functions

def to_lower (arg:str):
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
async def GetForecast(ctx, area: to_lower=None, date: to_lower=None, time: to_lower=None, duration: int=None):
    f""" Gets a weather forecast from Mabinogi World Weather API.
    
    Usage: 
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
    if ctx.message.author.id == Users['rice']:
        response += 'You are: 101% Smelly! Oh god it\'s like a diaper filled with Indian food...'
    else:
        response += f'You are: {random.randint(0,100)}% Smelly! ' + random.choice(_quips)
    await ctx.send(response)
    
@bot.command(name='role')
@commands.has_permissions(manage_roles=True)
async def AssignCosmeticRoles(ctx, role: discord.Role):
    f""" Usage: {prefix}role
    
    Available roles:
    Basic, Intermediate, Advanced, Hardmode, Elite
    Archer, Warrior, Mage, Alchemist
    Shinecraft - for guild Minecraft server"""
    try:
            
        if ctx.message.guild is None or ctx.message.guild != bot.get_guild(Guilds["Shine"]):
            # This function for Shine guild only
            return
        
        if bot.get_guild(Guilds["Shine"]).get_role(Roles["Member"]) not in ctx.message.author.roles:
                await ctx.send(f"You must be a member to use this command!")
                return
            
        pool = [bot.get_guild(Guilds["Shine"]).get_role(x) for x in CosmeticRoles.values()]
        if role not in pool:
            await ctx.send("This role isn't a valid Cosmetic Role. Acceptable roles:\n```" \
                           + (', '.join([str(x) for x in CosmeticRoles])) + '```')
            return
        
        if role not in ctx.message.author.roles:
            await ctx.message.author.add_roles(role)
            await ctx.send(f"Added role {role.name} {ctx.message.author.mention}")
            return
        else:
            await ctx.message.author.remove_roles(role)
            await ctx.send(f"Removed role {role.name} {ctx.message.author.mention}")
            return   
    except discord.Forbidden:
        await ctx.send(f"Whoops! I don't have the permissions to do that.") 
        
@AssignCosmeticRoles.error
async def roles_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("No role by that name was found. Acceptable roles:\n```" \
                       + (', '.join([str(x) for x in CosmeticRoles])) + '```')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Whoops! I don't have the permissions to do that.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Usage: {prefix}role <role>\nAcceptable roles:```" \
                       + (', '.join([str(x) for x in CosmeticRoles])) + '```')
    else:
        await ctx.send(error)
        
        
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

bot.run(token)