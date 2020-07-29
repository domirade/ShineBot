import config
import logging
import shinebot_token
from discord.ext import commands, tasks
from discord import File
import discord
from sqlite import insert_table, read_table, wipe_table
import sqlite3
import asyncio
from datetime import datetime
import math
import random
from daily_shadow_mission import daily_async

# standard logging stuff
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='shinebot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#create Table(s) if they dont exist yet
def create_table():
    conn = None
    try:
        conn = sqlite3.connect('idea.db')
    except sqlite3.Error as e:
        print("unexppected error has occured while attem,pting to connect to the db: ", e)

    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(""" CREATE TABLE IF NOT EXISTS IDEAS (
                                        ID integer PRIMARY KEY AUTOINCREMENT,
                                        NAME text NOT NULL,
                                        IDEA text
                                    ); """)
            print('table created')
            
        except sqlite3.Error as e:
            print("Something has gone wring while trying to create a table: ", e)
    else:
        print("Connection creation failed, try again later or whatever zzzz")
    conn.close()

create_table()


# initialize command prefix based on the mode

prefix = '!' if config.mode == 'dev' else '%'

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   case_insensitive=True)

# commands

@bot.event
async def on_ready():
    print('test on ready')

async def time_check():
    await bot.wait_until_ready()
    while not bot.is_closed():
        what_day = datetime.today().weekday()
        if (what_day == 5): #0=monday, 6-sunday, 5=saturday
            now=datetime.strftime(datetime.now(),'%H:%M')
            if (now == '19:00'): #7pm
                results = await read_table()
                meetingChann = bot.get_channel(700852121150554133)
                await meetingChann.send('This week\'s suggestion list: \n')
                for i in results:
                    await  meetingChann.send(i)
                await wipe_table()
                time = 90 #prevent checking for date until after the time has passed to prevent multi posts
            else:
                time = 5 #if not time wait to check again for 5 seconds
        else:
            time = 9001 #if not even the correct day of the week, take a long break
        await asyncio.sleep(time)

bot.loop.create_task(time_check())

        
@bot.command(name='ping')
async def heartbeat(ctx):
    """ Check if the bot's alive """
    response = 'PONG!\n'
    if config.mode == 'dev':
        response += str(bot.latency)
    await ctx.send(response)
        
@bot.command(name='daily')
async def DailyShadowMission(ctx, *args):
    """ args will be parsed in func `daily()` """
    response = await daily_async.daily(*args)
    await ctx.send(response)

@bot.command()
async def logout(ctx):
    """ If this is dev, log out and exit """
    if config.mode != 'dev':
        return
    await ctx.send('Logging out now...')
    await bot.logout()

@bot.command(name='parrot')
async def parrot(ctx, *args):
	await ctx.send(' '''.join(args))

@bot.command(name='waifu')
async def waifu(ctx):
    await ctx.send('https://i.imgur.com/eWD6Jkk.jpg')

@bot.command(name='faint')
async def faint(ctx):
    await ctx.send('sigh... what did he do now?')

@bot.command(name='mitch')
async def mitch(ctx):
    await ctx.send('https://www.youtube.com/watch?v=yOMj7WttkOA')

@bot.command(name='meta')
async def metaSpot(ctx):
    await ctx.send('m e t a s p o t')

@bot.command(name='eryse')
async def eryse(ctx):
    await ctx.send('*still buying*')

@bot.command(name='kyou')
async def kyoupon(ctx):
    await ctx.send('pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon pon ')

@bot.command(name='domi')
async def domi(ctx):
    await ctx.send('https://www.youtube.com/watch?v=dpqxSBclqWs')

@bot.command(name='millie')
async def millie(ctx):
    await ctx.send('Phweeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

@bot.command(name='sellout')
async def sellout(ctx):
    await ctx.send('This message brought to you by Chili\'s, cause fuck Applebees')

@bot.command(name='repost')
async def repost(ctx):
    await ctx.send('https://www.youtube.com/watch?v=4feUSTS21-8')

@bot.command(name='vlad')
async def vlad(ctx):
    await ctx.send('*yawn*')

@bot.command(name='idea')
async def ideaCreate(ctx, *args):
    tweetlen = map(str,args)
    dummy = ' '.join(tweetlen)
    if(len(dummy) >= 280):
        stringThing = 'Idea too long, the current limit is 280 characters including spaces, please submit a shorter message or use pastebin and submit the url. Your idea\'s character length was: ' + str(len(dummy))
        await ctx.send(stringThing)
    else:
        await insert_table(ctx.author.name, ' '''.join(args))
        await ctx.send('Idea recorded')

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
    print('Logged in as {0.user}'.format(bot))
    print('ShineBot version {0.version} build {0.build}'.format(config))

bot.run(shinebot_token.token)
