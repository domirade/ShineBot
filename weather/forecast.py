import asyncio
import aiohttp
import json
from dateutil.parser import *
from datetime import *

session = None
response = None
url = "http://mabi.world/api/forecast/"

emoji = {"unknown": "❓",
         "sunny": "☀",
         "cloudy": "☁",
         "rain": "🌧️",
         "thunder": "⛈"
         }

def _EmojiForWeather(i:int) -> str:
   if i == -9:
      return emoji["unknown"]
   elif i == -8:
      return emoji["sunny"]
   elif i in range(-7,0):
      return emoji["cloudy"]
   elif i in range(0, 20):
      return emoji["rainy"]
   elif i == 20: # range's second parameter is exclusive
      return emoji["thunder"]
      

async def get(_area, _day, _time, _duration) -> str:
   
   # limit duration where appropriate
   if _duration >= 24:
      _duration = 24
   
   if _area == "all" and _duration > 2:
      _duration = 2
      
   # mash our date arg into the right format
   try: 
      if _day in ('today','now'):
         _day = datetime.now(timezone.utcoffset(timedelta(hours=-4)))
      elif _day == "tomorrow":
         _day = datetime.now(timezone.utcoffset(timedelta(hours=-4))) + timedelta(days=1)
      elif _day == "yesterday":
         _day = datetime.now(timezone.utcoffset(timedelta(hours=-4))) - timedelta(days=1)
      else :
         _day = date.fromisoformat(_day)
   except TypeError:
      return f"Invalid argument: {_day}, try 'today', 'tomorrow', or YYYY-MM-DD format."
   finally:
      if _day is datetime:
         _day = _day.date()
         
   # mash our time arg into the right format
   try:
      if _time == None:
         _time = time(hour=0,minute=0,second=0) # midnight
      else:
         _time = parser.parse(_time, ignoretz=True).time()
   except TypeError:
      return f"Invalid argument: {_time}, make sure it's 1:00pm or 13:00 format."
   
   
   return f"Area `{_area}`, Day `{_day}`, Time `{_time}`, Duration `{_duration}`\n" +  f"Combined Parse: `{datetime(_day,_time)}`"  