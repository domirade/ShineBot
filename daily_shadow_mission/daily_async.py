import aiohttp
import asyncio
import datetime
import json
import re
from discord import Embed, Color
from discord.ext import commands, tasks

from .i18n import KR, JP, EN, ZH_TW, ZH_CN
from enums import Channels


class DailyMission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.today = self.server_time().date()
        # self.url = "https://mabi-api.sigkill.kr/get_todayshadowmission/{}?ndays={}"
        self.url = "https://mabi.world/sm/mww/{}/{}/{}.json"
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
        date = self.server_time().date()
        if date == self.today:
            pass
        else:
            channel = self.bot.get_channel(Channels["LFG"])
            response = await self.daily_mission()
            await channel.send(embed=response)
            self.today = date

    @staticmethod
    def server_time() -> str:
        # 4 hours for the UTC-4 timezone, 7 hours for the daily mission refresh offset(7:00 AM)
        now = datetime.datetime.utcnow() - datetime.timedelta(hours=4) - \
            datetime.timedelta(hours=7)
        return now

    @staticmethod
    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def daily_mission(self, *args, days: int = 1) -> Embed:
        try:
            time_match_pattern = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
            server_time = self.server_time()
            year, month, day = server_time.year, server_time.month, server_time.day
            # matching the date argument
            for this_arg in args:
                match = time_match_pattern.match(this_arg)
                if match:
                    # date = f"{match[1]}-{int(match[2])}-{int(match[3])}"
                    year, month, day = match[1], match[2], match[3]
                    break
            # generate url
            url = self.url.format(year, month, day)
            # send request to daily SM API
            async with aiohttp.ClientSession() as session:
                response = json.loads(await self.fetch(session, url))
            taillteann = response["Taillteann"]["Normal"]
            tara = response["Tara"]["Normal"]
            # matching the i18n argument
            if {"JP", "jp"}.intersection(set(args)):
                taillteann = JP[taillteann]
                tara = JP[tara]
            elif {"KR", "kr"}.intersection(set(args)):
                taillteann = KR[taillteann]
                tara = KR[tara]
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
            description=f"Date: {year}-{month}-{day}",
            color=Color.gold()
        )
        embed.add_field(name="Taillteann", value=taillteann, inline=False)
        embed.add_field(name="Tara", value=tara, inline=False)
        # embed.set_footer(text="Data source: https://mabi-api.sigkill.kr/")
        return embed
