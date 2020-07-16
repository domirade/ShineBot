import config
import logging
import shinebot_token
from discord.ext import commands

from daily_shadow_mission import daily_async

# standard logging stuff
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='shinebot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# initialize command prefix based on the mode

prefix = '!'
if config.mode != 'dev':
    prefix = '%'

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

# commands

@bot.command(name='ping')
async def heartbeat(ctx):
    """ Check if the bot's alive """
    response = 'PONG!\n'
    if config.mode == 'dev':
        response += str(bot.latency)
    await ctx.send(response)
        
@bot.command(name='daily')
async def DailyShadowMission(ctx, arg='en'):
    pass
    """ Check mabinogi.sigkill.kr/todaymission/ in provided language.
    today_mission = await daily_async.daily(arg)
    await ctx.send(today_mission)
    """

@bot.command()
async def logout(ctx):
    """ If this is dev, log out and exit """
    if config.mode != 'dev':
        return
    await ctx.send('Logging out now...')
    await bot.logout()
    

# finish initialization

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print('ShineBot version {0.version} build {0.build}'.format(config))



bot.run(shinebot_token.token)
