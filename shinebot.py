import logging
import random
import discord
from enums import Guilds, Users, Roles, CosmeticRoles, Channels
from discord.ext import commands
import math
import config
import version
from authtoken import token
from daily_shadow_mission.daily_async import DailyMission
from weather.forecast import Weather

    
# standard logging stuff

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
filename = 'shinebottest.log' if config.mode == 'dev' else 'shinebot.log'
handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

__version__ = version.version
mode = config.mode

# initialize command prefix based on the mode

prefix = config.testprefix if config.mode == 'dev' else '%'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   case_insensitive=True)

# helper functions


def titlecase (arg:str) -> str:
    return arg.title()

# cogs

bot.add_cog(DailyMission(bot))
bot.add_cog(Weather(bot))

# commands

@bot.command(name='ping')    
async def heartbeat(ctx):
    """ Asks the bot for a response.
    
    "Hello? Are you still there?" 
    """
    response = 'pong\n'
    if config.mode == 'dev':
        response += f"Latency {math.trunc(bot.latency*1000)}ms\n"
        response += f'This instance run by {config.tester}'
    await ctx.send(response)


@bot.command()
async def logout(ctx) -> None:
    """ Logs out the bot. Authorized users only. """
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
async def AssignCosmeticRoles(ctx, role: titlecase):
    """ Assign or remove a cosmetic role. 
    
    Available roles: See #welcome
    """
    try:
        converter = commands.RoleConverter()
        role = await converter.convert(ctx, str(CosmeticRoles[role]))
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
    except discord.Forbidden as ex:
        await ctx.send(ex)
        
@AssignCosmeticRoles.error
async def roles_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("No role by that name was found. Acceptable roles:\n```" \
                       + (', '.join([str(x) for x in CosmeticRoles])) + '```')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Whoops! I don't have the permissions to do that.\n" + error)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Usage: {prefix}role <role>\nAcceptable roles:```" \
                       + (', '.join([str(x) for x in CosmeticRoles])) + '```')
    else:
        await ctx.send(error)
        
        
        # finish initialization

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
        await channel.send(f"{bot.user} v{__version__}-{mode} initialized or reconnected.")

bot.run(token)
