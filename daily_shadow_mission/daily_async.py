import aiohttp
import asyncio
import datetime
import json
import re

from .i18n import JP, EN, ZH_TW, ZH_CN

URL = "https://mabi-api.sigkill.kr/get_todayshadowmission/{}?ndays={}"

def today():
    ## 4 hours for the UTC-4 timezone, 7 hours for the daily mission refresh offset(7:00 AM)
    now = datetime.datetime.utcnow() - datetime.timedelta(hours=4) - datetime.timedelta(hours=7)   
    return f"{now.year}-{now.month}-{now.day}"

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def daily(*args, days:int=1):
    try:
        time_match_pattern = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
        date = today()
        # matching the date argument
        for this_arg in args:
            match = time_match_pattern.match(this_arg)
            if match:
                date = f"{match[1]}-{int(match[2])}-{int(match[3])}"
                break
        # generate url
        url = URL.format(date, days)
        # send request to daily SM API
        async with aiohttp.ClientSession() as session:
            response = json.loads(await fetch(session, url))
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
        output = f"**Taillteann**: {taillteann}, **Tara**: {tara}"
    except Exception:
        import traceback
        error_msg = traceback.format_exc()
        output = f"Can't fetch the daily SM, the error message is {error_msg}"
    return output

async def main(*args):
    result = await daily(*args)
    print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("jp", "2020-07-31"))
