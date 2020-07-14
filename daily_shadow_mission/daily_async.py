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

async def daily(date:str=today(), i18n="EN", days:int=1):
    async with aiohttp.ClientSession() as session:
        url = URL.format(date, days)
        response = json.loads(await fetch(session, url))
        taillteann = response[0]["Taillteann"]["normal"]["name"]
        tara = response[0]["Tara"]["normal"]["name"]
        if i18n == "EN":
            taillteann = EN[taillteann]
            tara = EN[tara]
        elif i18n == "JP":
            taillteann = JP[taillteann]
            tara = JP[tara]
        elif i18n == "ZH_TW":
            taillteann = ZH_TW[taillteann]
            tara = ZH_TW[tara]
        elif i18n == "ZH_CN":
            taillteann = ZH_CN[taillteann]
            tara = ZH_CN[tara]
        return f"`Taillteann`: {taillteann}, `Tara`: {tara}"

async def main():
    result = await daily()
    print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
