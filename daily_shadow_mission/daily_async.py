import aiohttp
import asyncio
import datetime
import json
import re
from discord import Embed, Color
from discord.ext import commands, tasks

from .i18n import JP, EN, ZH_TW, ZH_CN
from enums import Channels


class DailyMission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.today = self.today_without_zero()
        self.url = "https://mabi-api.sigkill.kr/get_todayshadowmission/{}?ndays={}"
        self.broadcast.start()

    @commands.command()
    async def daily(self, ctx, *args):
        """ Gets the current Daily Shadow Missions.

        Usage:
        daily
        daily <YYYY-MM-DD>

        Example:
        daily 2020-08-16
        """
        response = await self.daily_mission(*args)
        await ctx.send(embed=response)

    @tasks.loop(minutes=10)
    async def broadcast(self):
        date = self.today_without_zero()
        if date == self.today:
            pass
        else:
            channel = self.bot.get_channel(Channels["LFG"])
            response = await self.daily_mission()
            await channel.send(embed=response)
            self.today = date

    @staticmethod
    def today_without_zero() -> str:
        # 4 hours for the UTC-4 timezone, 7 hours for the daily mission refresh offset(7:00 AM)
        now = datetime.datetime.utcnow() - datetime.timedelta(hours=4) - \
            datetime.timedelta(hours=7)
        return f"{now.year}-{now.month}-{now.day}"

    @staticmethod
    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def daily_mission(self, *args, days: int = 1) -> Embed:
        try:
            time_match_pattern = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
            date = self.today_without_zero()
            # matching the date argument
            for this_arg in args:
                match = time_match_pattern.match(this_arg)
                if match:
                    date = f"{match[1]}-{int(match[2])}-{int(match[3])}"
                    break
            # generate url
            url = self.url.format(date, days)
            # send request to daily SM API
            async with aiohttp.ClientSession() as session:
                response = json.loads(await self.fetch(session, url))
            taillteann = response[0]["Taillteann"]["normal"]["name"]
            tara = response[0]["Tara"]["normal"]["name"]
            # matching the i18n argument
            if {"JP", "jp"}.intersection(set(args)):
                taillteann = JP[taillteann]
                tara = JP[tara]
            elif {"KR", "kr"}.intersection(set(args)):
                pass
            elif {"ZH_CN", "zh_cn", "CN", "cn"}.intersection(set(args)):
                taillteann = ZH_CN[taillteann]
                tara = ZH_CN[tara]
            elif {"ZH_TW", "zh_tw", "TW", "tw"}.intersection(set(args)):
                taillteann = ZH_TW[taillteann]
                tara = ZH_TW[tara]
            else:
                taillteann = EN[taillteann]
                tara = EN[tara]
        except json.decoder.JSONDecodeError:
            embed = Embed(
                title="Error Occurred While Fetching Daily Shadow Missions",
                color=Color.red()
            )
            embed.add_field(name="Error message:",
                            value="API is down or returned unexpected data", inline=False)
            return embed
        except Exception:
            import traceback
            error_msg = traceback.format_exc()
            embed = Embed(
                title="Error Occurred While Fetching Daily Shadow Missions",
                color=Color.red()
            )
            embed.add_field(name="Error message:",
                            value=error_msg, inline=False)
            embed.set_footer(
                text="please contact shinebot developers @ShineBot dev")
            return embed
        embed = Embed(
            title="Daily Shadow Missions",
            description=f"Date: {date}",
            color=Color.gold()
        )
        embed.add_field(name="Taillteann", value=taillteann, inline=False)
        embed.add_field(name="Tara", value=tara, inline=False)
        # embed.set_footer(text="Data source: https://mabi-api.sigkill.kr/")
        return embed
