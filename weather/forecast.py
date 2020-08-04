import asyncio
import aiohttp
import json
import enum
from datetime import *
from dateutil import tz
from dateutil.parser import parse

@enum.unique
class Emoji(enum.Enum):
   unknown = "❓"
   sunny = "☀"
   cloudy = "☁"
   rainy = "🌧"
   thunder = "⛈"
   def get(i:int) -> str:
      """ Gets the emoji corresponding to the integer argument. """
      if i == -9:
         return Emoji.unknown.value
      elif i == -8:
         return Emoji.sunny.value
      elif i in range(-7,0):
         return Emoji.cloudy.value
      elif i in range(0,20):
         return Emoji.rainy.value
      elif i == 20:
         return Emoji.thunder.value
   
async def apiRequest(url, params):
   """ Submit request with parameter and retrieve JSON object. """
   async with aiohttp.ClientSession() as session:
      async with session.get(url, params=params) as resp:
         return (await resp.json() )

async def get(_area, _date, _time, _duration) -> str:
   # initialize defaults INSIDE function (or else)
   if _area is None: _area = "all"
   if _date is None: _date = "now"
   if _duration is None: _duration = 2
   
   _api = "http://mabi.world/api/forecast/"
   _tz = tz.gettz('America/New_York')
   _start = datetime.now(_tz)
   result = ''
   
   # limit duration where appropriate
   if _duration > 24:
      _duration = 24
   elif not isinstance(_duration, int):
      return f"Invalid argument: `{_duration}`, must be between 1 and 24"
   
   if _area == "all" and _duration > 2:
      _duration = 2
      
   # figure out the area we are filtering down to, if possible
   # the second element, or types[x][1], should be the 'descriptive' name
   
   types = {
   'type1':['1', 'Tir Chonaill / Dugald', 'tir', 'dugald'],
   'type2':['2', 'Dunbarton / Gairech', 'dunbarton', 'dunby', 'dunb', 'dun', 'gairech', 'fiodh', 'cobh'],
   'type3':['3', 'Bangor', 'bangor'],
   'type4':['4', 'Emain Macha', 'emain'],
   'type5':['5', 'Sen Mag Prairie', 'senmag', 'sen_mag'],
   'type6':['6', 'Port Ceann / Morva Aisle', 'ceann' 'morva'],
   'type7':['7', 'Rano', 'rano', 'nubes', 'solea'],
   'type8':['8', 'Connous', 'connous', 'filia', 'rupes'],
   'type9':['9', 'Courcle', 'courcle', 'cor', 'lappa', 'herba', 'cenae'],
   'type10':['10', 'Physis', 'physis', 'vales', 'zardine', 'calida', 'raspa', 'renes'],
   'type11':['11', 'Shadow Realm', 'shadow'],
   'type12':['12', 'Taillteann, Sliab, Abb Neagh', 'taillteann', 'taill', 'tail', 'tara', 'corrib', 'blago', 'sliab', 'abb', 'neagh', 'abbneagh'],
   'type13':['13', 'Unknown/Unused']
   }
   
   _of = None
   if _area != "all":
      _of = [t for t, n in types.items() if _area in n]
      if _of is None:
         return f"Couldn't find an area matching: {_area}"
      
   # Construct an aware datetime based on the day and time
   
   try: 
      if _date in ('today','now'):
         _date = datetime.now(_tz).date()
      elif _date == "tomorrow":
         _date = datetime.now(_tz).date() + timedelta(days=1)
      elif _date == "yesterday":
         _date = datetime.now(_tz).date() - timedelta(days=1)
      else :
         _date = date.fromisoformat(_date)
   except TypeError:
      return (f"Invalid argument: `{_date}`, try `today`, `tomorrow`, or YYYY-MM-DD format.\n"
              f"{sys.exc_info()[0]}\n" )
         
   # mash our time arg into the right format
   try:
      if _time is not None:
         _time = parse(_time, parserinfo=None, ignoretz=True).time()
         _start = datetime.combine(_date, _time, tzinfo=_tz)
         # _start = _tz.localize(_start)
         result += f"Method 2 Parse called: {_start}\n"
      else:
         _start = datetime.combine(_date, time(0,0,0), tzinfo=_tz)
         # _start = _tz.localize(_start)
         result += f"Method 1 Parse called: {_start}\n"
   except TypeError:
      result += (f"Something went wrong with time! Time `{_time}` Start `{_start}`\n"
              f"{sys.exc_info()[0]}") 
   except Exception as ex:
      return f"Could not parse argument: `{_time}`, please double check the format." \
             + ex
   
   result += f"Debug: Area `{_area}`, Day `{_date}`, Time `{_time}`, Duration `{_duration}`\n" \
      + f"_start: `{_start.isoformat()}` _tz: {_tz}"
   
   # add 3 hours to account for the API only returning results in Pacific time
   _start += timedelta(hours=3)
   
   x = str(_start).rpartition('-')
      
   params = {'from': x[0].replace(" ","T"), 
             'tz': 'America/New_York',
             'duration': _duration * 3}
   
   if _of is not None:
      params['of'] = _of
      
   print (params)
      
   response = await apiRequest(_api, params)
   
   if not response["forecast"]:
      return "Something went wrong: forecast is empty"
   else:
      for key in response["forecast"]:
         if key.startswith('type'):
            result += types[key][1] + ": "
            for i in response["forecast"][key]:
               result += Emoji.get(i)
            result += "\n"
   
   
   return result
   
   