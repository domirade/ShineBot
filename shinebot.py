import config
import logging
import shinebot_token
from discord.ext import commands, tasks
from discord import File
import discord
from sqlite import insert_table, read_table
import sqlite3
import asyncio
import aioschedule as schedule
from datetime import datetime

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

prefix = '!'
if config.mode != 'dev':
    prefix = '%'

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

# commands

async def weeklyIdeas():
    await read_table()
    await wipe_table()

async def testTimer(n):
    for i in range(n):
        print("testing timer")


##schedule.every().saturday.at("19:00").do(weeklyIdeas)
##
##schedule.every().day.at("14:00").do(testTimer,3)
##schedule.every().day.at("14:03").do(testTimer,4)
##schedule.every().day.at("14:04").do(testTimer,5)
##schedule.every().day.at("14:05").do(testTimer,6)
##schedule.every().day.at("14:06").do(testTimer,7)
##
##loop = asyncio.set_event_loop()
##while True:
##    loop.run_until_complete(schedule.run_pending())

print(datetime.strftime(datetime.now(),'%H:%M'))
print(datetime.today().weekday()) 

@bot.event
async def on_ready():
    print('test on ready')

async def time_check():
    await bot.wait_until_ready()
    while not bot.is_closed():
        what_day = datetime.today().weekday()
        if (what_day == 4):
            now=datetime.strftime(datetime.now(),'%H:%M')
            if (now == '15:00'):
                print('test timer')
                time = 90
            else:
                time = 1
        else:
            time = 1
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

@bot.command(name='parrot')
async def parrot(ctx, *args):
	await ctx.send(' '''.join(args))

@bot.command(name='waifu')
async def waifu(ctx):
    await ctx.send('https://i.imgur.com/eWD6Jkk.jpg')

@bot.command(name='faint')
async def faint(ctx):
    await ctx.send('sigh... what did he do now?')

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


##@bot.command(name='idea')
##async def ideaWrite(ctx, *args):
##    with open('idealist.txt','a') as file:
##        file.write(' '''.join(args) + '\n') #and no, file.close() is not needed
##    await ctx.send('message recorded~')    
##
##    
##@bot.command(name='print')
##async def ideaPrint(ctx):
##    await ctx.send('idealist',file=File('idealist.txt'))
##    
##@bot.command(name='wipe')
##async def ideaWipe(ctx):
##    open("idealist.txt", "w").close()
##    await ctx.send('idea list deleted')



@bot.command(name='idea')
async def ideaCreate(ctx, *args):
    await insert_table(ctx.author.name, ' '''.join(args))
    await ctx.send('Idea recorded')

@bot.command(name='print')
async def ideaRead(ctx):
    await ctx.send('Idea list printed on console')
    await read_table()
    print("print test")

#@bot.command(name='')
#async def (ctx):

    
# finish initialization

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print('ShineBot version {0.version} build {0.build}'.format(config))



bot.run(shinebot_token.token)
