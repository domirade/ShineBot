import discord
import config
import logging
import random

from daily_shadow_mission import daily_async

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='shinebot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    # do not talk to yourself that's crazy
    if message.author == client.user:
        # print(message.author)
        return
    
    # sass mentions, and be rude to Domi
    if client.user.mention in message.mentions:
        response = random.choice(['no u', 'bet', 'Neigh!'])
        if message.author.id == 146191479746854913 and message.author.discriminator == '0413': # Domirade#0413
            response = config.rude
        await message.channel.send(message.author.mention + response)
        return
            

    # babby's first test command
    if message.content.startswith('%ping'):
        await message.channel.send('PONG!')
        return

    # daily SM
    if message.content.startswith('%daily'):
        today_mission = await daily_async.daily()
        await message.channel.send(today_mission)
        return
    
    if message.content.startswith('%daily_jp'):
        today_mission = await daily_async.daily(i18n="JP")
        await message.channel.send(today_mission)
        return

    if message.content.startswith('%daily_kr'):
        today_mission = await daily_async.daily(i18n="KR")
        await message.channel.send(today_mission)
        return

    if message.content.startswith('%daily_cn'):
        today_mission = await daily_async.daily(i18n="ZH_CN")
        await message.channel.send(today_mission)
        return

client.run(config.token)
