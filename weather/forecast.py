import aiohttp
import json
import enums
from datetime import *
from dateutil import tz
from dateutil.parser import parse, ParserError
from discord.ext import commands
from discord.ext.commands import BadArgument
import config

class Weather(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.api = "http://mabi.world/api/forecast/"
      
      # the second element, or types[x][1], should be the 'descriptive' name
      
      self.types = {
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
      'type12':['12', 'Taillteann/Tara Region', 'taillteann', 'taill', 'tail', 'tara', 'corrib', 'blago', 'sliab', 'abb', 'neagh', 'abbneagh'],
      'type13':['13', 'Unknown/Unused']
      }
      
   def to_lower (arg:str) -> str:
      return arg.lower()
   
   @commands.command(name='whenrain')
   async def GetNextRain(self, ctx, area: to_lower=None):
      """ Gets the next rain (of any severity) for a given area.
   
      Usage:
      whenrain <area>
   
      Examples:
      whenrain
      whenrain dunbarton
   
      Notes:
      If run without a paremeter, will find the next rain _anywhere_
      Remember: API doesn't discriminate between different degrees of rain strength.
      If you're looking for the biggest bonus for non-Alchemy lifeskills, try whenthunder instead.
      """
      async with ctx.message.channel.typing():
         params = await self.nextParams("rain", area)
         response = await self.apiRequest(params)
         await ctx.send(await self.parseUpcoming(response, area))
      return
   
   @commands.command(name='whenthunder')
   async def GetNextThunder(self, ctx, area: to_lower=None):
      """ Gets the next thunder for a given area. 
   
      Usage:
      whenthunder <area>
   
      Examples:
      whenthunder
      whenthunder taillteann
   
      Notes:
      If run without a parameter, will find the next thunder _anywhere_
   
      """
      async with ctx.message.channel.typing():
         params = await self.nextParams("thunder", area)
         response = await self.apiRequest(params)
         await ctx.send(await self.parseUpcoming(response, area))
      return
   
   @commands.command(name='weather')
   async def GetForecast(self, ctx, area: to_lower=None, date: to_lower=None, time: to_lower=None, duration: int=None):
      """ Gets a weather forecast from Mabinogi World Weather API. 
   
      Usage: 
      weather <area>
      weather <area> <date> <time>
      weather area now <duration>
      weather <area> <date> <time> <duration>
   
      Examples:
      weather rano tomorrow
      weather taillteann today 18:00 6
   
      If run with no arguments, defaults to a 2-hour forecast of all regions.
      This is the same as running `%weather all now`
   
      Area defaults to "all" if omitted.
      It accepts the numeric region IDs as well as most common names and nicknames for places.
   
      Date defaults to "now" if omitted.
      It can otherwise accept 'tomorrow' 'yesterday' and any YYYY-MM-DD format.
   
      Time defaults to midnight if omitted.
      It accepts a value in HH:MM format. If date is "now", you can specify duration as integer instead.
   
      Duration is the length of the forecast expressed in IRL hours (three 20-minute segments each)
      It's default to 24 hours for a single area and limited to 2 hours for all of them.
      """
      async with ctx.message.channel.typing():
         params = await self.forecastParams(area, date, time, duration)
         response = await self.apiRequest(params)
         response = await self.parseForecast(response)
         await ctx.send(response)
      return
   
   @GetForecast.error
   async def forecast_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
         await ctx.send("Bad argument: double check the order of parameters.")
      else:
         print(error)
   
   def _thirdround(self, dt) :
      return datetime(dt.year, dt.month, dt.day, dt.hour, 20 * (dt.minute // 20), 0, 0)

   async def apiRequest(self, params):
      """ Submit request with parameters and retrieve JSON object. """
      async with aiohttp.ClientSession() as session:
         async with session.get(self.api, params=params) as resp:
            return (await resp.json() )

   async def nextParams(self, _weather, _area) -> dict:
      """ Create a 'params' dict to get upcoming weather. """
      params = await self.forecastParams(_area, None, None, None)
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



   async def forecastParams(self, _area, _date, _time, _duration) -> dict:
      """ Create a 'params' dict to get a forecast with. """
      # initialize defaults INSIDE function (or else)
      if _area is None:
         _area = "all"
      if _date is None:
         _date = "now"
      if _duration is None:
         _duration = 24
         
      try:
         if _date in ("now", "today", "tomorrow", "yesterday") and _time.isdigit():
            _duration = int(_time)
      except:
         pass
      
      _tz = tz.gettz('America/New_York')
      _start = None
      result = ''
      
      # limit duration where appropriate
      
      if not isinstance(_duration, int):
         return f"Invalid argument: `{_duration}`, must be between 1 and 24"
      elif _duration > 24:
         _duration = 24
      
      if _area == "all" and _duration > 2:
         _duration = 2
      if _duration < 1:
         result += "Duration too low, clamped to 1"
         _duration = 1
         
      # figure out the area we are filtering down to, if possible
      
      _of = None
      if _area == "now":
         raise BadArgument
      elif _area != "all":
         _of = [key for key, value in self.types.items() if _area in value]
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
         return f"Could not parse time argument, please check format.\n" \
                + ex
      
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


   async def parseForecast(self, response) -> str:
      """ Format our JSON result into our output message. """
      
      result = ''
      if not response['from']:
         return f"Error! Invalid or unexpected response:\n{response}"
      
      _from = self._thirdround(datetime.fromisoformat(response['from']))
      
      result += f"Result as of {_from.date().isoformat()} {_from.time().isoformat(timespec='minutes')}:\n"
      
      if "forecast" in response:
         for key in response["forecast"]:
            if key.startswith('type'):
               t = _from
               result += '**' + self.types[key][1] + '**:\n'
               _list = []
               for count, element in enumerate(response["forecast"][key], 1):
                  temp = f"[{t.time().isoformat(timespec='minutes')}: {enums.Emoji.get(element)}]"
                  if count % 6 == 0 and len(response["forecast"][key]) > 6:
                     temp += "\n"
                  _list.append(temp)
                  t += timedelta(minutes=20)
               result += " ".join(_list)
               result += '\n'
                   
      return result

   async def parseUpcoming(self, response, area) -> str:
      """ Upcoming weather responses look a bit different. """
      
      result = ''
      if not response['from']:
         return f"Error! Invalid or unexpected response:\n{response}"
      
      _from = datetime.fromisoformat(response['from'])
      result += f"Result as of {_from.time().isoformat(timespec='minutes')}:\n"   
      
      if "next" in response:
            weather = enums.Emoji.get(response['next']['weather'])
            if area is None:
               # area was 'all'
               location = self.types[(response['next']['for'])][1]
               time = timedelta(minutes=response['next']['in'])
               when = _from + time
               
               result += (f"Next {weather} will be: {location} in {time}.\n" \
                          + f"(At: {when.isoformat()} EST)")
            else:
               # area was specific, we are filtering an 'each' request
               location = [key for key, value in self.types.items() if area in value]
               location = location[0]
               time = timedelta(minutes=response['next']['for'][location])
               when = _from + time
               
               result += (f"Next {weather} in {self.types[location][1]} will be: {time}.\n" \
                          + f"(At: {when.isoformat()} EST)")
               
      return result
   