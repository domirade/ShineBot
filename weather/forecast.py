import asyncio
import aiohttp
import json
import enum
from datetime import *
# from dateutil.parser import parse

_url = "http://mabi.world/api/forecast/"
session = aiohttp.ClientSession()
response = None

@enum.unique
class Emoji(enum.Enum):
   unknown = "❓"
   sunny = "☀"
   cloudy = "☁"
   rainy = "🌧"
   thunder = "⛈"
   def get(i:int) -> str:
      if i == -9:
         return Emoji.unknown
      elif i == -8:
         return Emoji.sunny
      elif i in range(-7,0):
         return Emoji.cloudy
      elif i in range(0,20):
         return Emoji.rainy
      elif i == 20:
         return Emoji.thunder

_offset = timezone(timedelta(hours=-4))

async def get(_area, _date, _time, _duration) -> str:
   # initialize defaults INSIDE function (or else)
   if _area is None: _area = "all"
   if _date is None: _date = "now"
   if _duration is None: _duration = 2
   _start = datetime.now()
   ret = ''
   
   # limit duration where appropriate
   if _duration > 24:
      _duration = 24
   elif not isinstance(_duration, int):
      return f"Invalid argument: `{_duration}`, must be between 1 and 24"
   
   if _area == "all" and _duration > 2:
      _duration = 2
      
   # Construct an aware datetime based on the day and time
   # TODO: Build out the acceptable list of values and reject command if not matched
   
   try: 
      if _date in ('today','now'):
         _date = datetime.now(_offset).date()
      elif _date == "tomorrow":
         _date = datetime.now(_offset).date() + timedelta(days=1)
      elif _date == "yesterday":
         _date = datetime.now(_offset).date() - timedelta(days=1)
      else :
         _date = date.fromisoformat(_date)
   except TypeError:
      return (f"Invalid argument: `{_date}`, try `today`, `tomorrow`, or YYYY-MM-DD format.\n"
              f"{sys.exc_info()[0]}\n" )
         
   # mash our time arg into the right format
   try:
      if _time is not None:
         _time = parse(_time, parserinfo=None, ignoretz=True).time()
         _start = datetime.combine(_date,_time)
         ret += f"Method 2 Parse called: {_start}\n"
      else:
         _start = datetime.combine(_start, time(0,0,0), tzinfo=_offset)
         ret += f"Method 1 Parse called: {_start}\n"
   except TypeError:
      ret += (f"Something went wrong with time! Time `{_time}` Start `{_start}`\n"
              f"{sys.exc_info()[0]}") 
   except:
      return f"Could not parse argument: `{_time}`, please double check the format."
   
   ret += f"Debug: Area `{_area}`, Day `{_date}`, Time `{_time}`, Duration `{_duration}`\n" \
      + f"_start: `{_start.isoformat()}`"
      
   return ret