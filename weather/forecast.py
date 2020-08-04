import aiohttp
import json
import enum
from datetime import *
from dateutil import tz
from dateutil.parser import parse, ParserError
from discord.ext.commands import BadArgument
import config

_api = "http://mabi.world/api/forecast/"

types = {
'type1':['1', 'Tir Chonaill / Dugald', 'tir', 'dugald'],
'type2':['2', 'Dunbarton / Gairech', 'dunbarton', 'dunby', 'dunb', 'dun', 'gairech', 'fiodh', 'cobh'],
'type3':['3', 'Bangor', 'bangor'],
'type4':['4', 'Emain Macha', 'emain'],
'type5':['5', 'Sen Mag Prairie', 'senmag', 'sen_mag'],
'type6':['6', 'Port Ceann / Morva Aisle', 'ceann', 'morva'],
'type7':['7', 'Rano', 'rano', 'nubes', 'solea'],
'type8':['8', 'Connous', 'connous', 'filia', 'rupes', 'longa'],
'type9':['9', 'Courcle', 'courcle', 'cor', 'lappa', 'herba', 'cenae', 'erkey', 'irai', 'waterfall'],
'type10':['10', 'Physis', 'physis', 'vales', 'zardine', 'calida', 'raspa', 'renes'],
'type11':['11', 'Shadow Realm', 'shadow'],
'type12':['12', 'Taillteann/Sliab Cuilin/Abb Neagh', 'taillteann', 'taill', 'tail', 'tara', 'corrib', 'blago', 'sliab', 'abb', 'neagh', 'abbneagh'],
'type13':['13', 'Unknown/Unused']
}

@enum.unique
class Emoji(enum.Enum):
   unknown = "❓"
   sunny = "☀"
   cloudy = "☁"
   rainy = "🌧"
   thunder = "🌩"
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
   
async def apiRequest(params):
   """ Submit request with parameters and retrieve JSON object. """
   async with aiohttp.ClientSession() as session:
      async with session.get(_api, params=params) as resp:
         return (await resp.json() )

async def nextParams(_weather, _area) -> dict:
   """ Create a 'params' dict to get upcoming weather. """
   params = await forecastParams(_area, None, None, None)
   params.pop('duration', None)
   params["next"] = _weather
   if "of" in params:
      # we selected a specific area
      params.pop('of', None)
      params["for"] = "each"
   else:
      params.pop('of', None)
      params["for"] = "all"
   
   return params
  
   

async def forecastParams(_area, _date, _time, _duration) -> dict:
   """ Create a 'params' dict to get a forecast with. """
   # initialize defaults INSIDE function (or else)
   if _area is None:
      _area = "all"
   if _date is None:
      _date = "now"
   if _duration is None:
      _duration = 2
   
   _tz = tz.gettz('America/New_York')
   _start = None
   result = ''
   
   # limit duration where appropriate
   if _duration > 24:
      _duration = 24
   elif not isinstance(_duration, int):
      return f"Invalid argument: `{_duration}`, must be between 1 and 24"
   
   if _area == "all" and _duration > 2:
      _duration = 2
   if _duration < 1:
      result += "Duration too low, clamped to 1"
      _duration = 1
      
   # figure out the area we are filtering down to, if possible
   # the second element, or types[x][1], should be the 'descriptive' name
   
   _of = None
   if _area == "now":
      raise BadArgument
   elif _area != "all":
      _of = [key for key, value in types.items() if _area in value]
      if _of is None or _of == []:
         return f"Couldn't find an area matching: {_area}"
      else:
         _of = _of[0]
      
   # Construct an aware datetime based on the day and time
   
   try: 
      if _date == "now":
         _date = datetime.now(_tz)
         _start = _date
      elif _date == "today":
         _date = datetime.now(_tz).date()
      elif _date == "tomorrow":
         _date = datetime.now(_tz) + timedelta(days=1)
      elif _date == "yesterday":
         _date = datetime.now(_tz) - timedelta(days=1)
      else :
         _date = date.fromisoformat(_date)
   except (TypeError, ValueError):
      return (f"Invalid argument: `{_date}`, try `today`, `tomorrow`, or YYYY-MM-DD format.\n"
              f"{sys.exc_info()[0]}\n" )
         
   # mash our time arg into the right format
   try:
      if _start is None:            
         if _time is not None:
            _time = parse(_time, parserinfo=None, ignoretz=True).time()
            _start = datetime.combine(_date, _time, tzinfo=_tz)
            # _start = _tz.localize(_start)
            result += f"Method 2 Parse called: {_start}\n"
         else:
            _start = datetime.combine(_date, time(0,0,0), tzinfo=_tz)
            # _start = _tz.localize(_start)
            result += f"Method 1 Parse called: {_start}\n"
   except (TypeError, ParserError):
      result += (f"Something went wrong with time! Time `{_time}` Start `{_start}`\n"
              f"{sys.exc_info()[0]}") 
   except Exception as ex:
      return f"Could not parse time argument, please check format."
   
   print(f"Debug: Area `{_area}`, Day `{_date}`, Time `{_time}`, Duration `{_duration}`\n" \
      + f"_start: `{_start.isoformat()}` _tz: {_tz} \n")
   
   # add 3 hours to account for the API only returning results in Pacific time
   _start += timedelta(hours=3)
   
   x = str(_start).rpartition('-')
      
   params = {'from': x[0].replace(" ","T"), 
             'tz': 'America/New_York',
             'duration': _duration * 3}
   
   if _of is not None:
      params['of'] = _of
      
   if config.mode == 'dev':
      print(result)
      print(params)
      
   return params
   
   
async def parseForecast(response) -> str:
   """ Format our JSON result. """
   
   result = ''
   if not response['from']:
      return f"Error! Invalid or unexpected response:\n{response}"
   
   _from = datetime.fromisoformat(response['from'])
   result += f"Result as of {_from.time()}:\n"
   
   if "forecast" in response:
      for key in response["forecast"]:
         if key.startswith('type'):
            result += types[key][1] + ':\n'
            for i in response["forecast"][key]:
               result += Emoji.get(i)
            result += '\n'    
            
   return result

async def parseUpcoming(response, area) -> str:
   """ Upcoming weather responses look a bit different. """
   
   result = ''
   if not response['from']:
      return f"Error! Invalid or unexpected response:\n{response}"
   
   _from = datetime.fromisoformat(response['from'])
   result += f"Result as of {_from.time()}:\n"   
   
   if "next" in response:
         weather = Emoji.get(response['next']['weather'])
         if area is None:
            # area was 'all'
            location = types[(response['next']['for'])][1]
            time = timedelta(minutes=response['next']['in'])
            when = _from + time
            
            result += (f"Next {weather} will be: {location} in {time}.\n" \
                       + f"(At: {when.isoformat()} EST)")
         else:
            # area was specific, we are filtering an 'each' request
            location = [key for key, value in types.items() if area in value]
            location = location[0]
            time = timedelta(minutes=response['next']['for'][location])
            when = _from + time
            
            result += (f"Next {weather} in {types[location][1]} will be: {time}.\n" \
                       + f"(At: {when.isoformat()} EST)")
            
   return result