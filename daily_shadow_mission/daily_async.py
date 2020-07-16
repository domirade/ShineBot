import aiohttp
import asyncio
import datetime
import json

from .i18n import JP, EN, ZH_TW, ZH_CN

URL = "https://mabi-api.sigkill.kr/get_todayshadowmission/{}?ndays={}"

def today():
    ## 4 hours for the UTC-4 timezone, 7 hours for the daily mission refresh offset(7:00 AM)
    now = datetime.datetime.utcnow() - datetime.timedelta(hours=4) - datetime.timedelta(hours=7)   
    return f"{now.year}-{now.month}-{now.day}"

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def daily(date:str=today(), i18n="EN", days:int=1, *args):
    async with aiohttp.ClientSession() as session:
        url = URL.format(date, days)
        response = json.loads(await fetch(session, url))
        taillteann = response[0]["Taillteann"]["normal"]["name"]
        tara = response[0]["Tara"]["normal"]["name"]
        if set("JP", "jp").intersection(set(args)):
            taillteann = JP[taillteann]
            tara = JP[tara]
        elif set("KR", "kr").intersection(set(args)):
            pass
        elif set("ZH_CN", "zh_cn", "CN", "cn").intersection(set(args)):
            taillteann = ZH_CN[taillteann]
            tara = ZH_CN[tara]
        elif set("ZH_TW", "zh_tw", "TW", "tw").intersection(set(args)):
            taillteann = ZH_TW[taillteann]
            tara = ZH_TW[tara]
        else:
            taillteann = EN[taillteann]
            tara = EN[tara]
        return f"**Taillteann**: {taillteann}, **Tara**: {tara}"

async def main():
    result = await daily()
    print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
