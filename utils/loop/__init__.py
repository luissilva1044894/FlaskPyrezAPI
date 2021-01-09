#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import sys

def get(force_fresh=False, debug=False):
  if not debug:
    try:
      import uvloop
    except ImportError:
      print('>>> Using asyncio')
      asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    else:
      #uvloop.install()
      print('>>> Using uvloop')
      asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
      #asyncio.set_event_loop(uvloop.new_event_loop())
  #loop.set_debug(False)
  if sys.platform == 'win32':
    if not force_fresh and isinstance(asyncio.get_event_loop(), asyncio.ProactorEventLoop) and not asyncio.get_event_loop().is_closed():
      return asyncio.get_event_loop()
    return asyncio.ProactorEventLoop()
  if force_fresh or asyncio.get_event_loop().is_closed():
    return asyncio.new_event_loop()#asyncio.get_event_loop_policy().new_event_loop() | asyncio.set_event_loop(asyncio.new_event_loop())
  return asyncio.get_event_loop()

def run(*args):
  def get_future(args):
    coros = list(filter(inspect.iscoroutine, args))
    if coros and isinstance(coros, (tuple, list)):
      if len(coros) > 1:
        return asyncio.gather(*coros)
      return coros[0]
    return coros
  #loop = get()
  #loop.run_until_complete(get_future(args))
  return get().run_until_complete(get_future(args))

def fire_and_forget(f):
  def wrapped(*args, **kw):
    return asyncio.get_event_loop().run_in_executor(None, f, *args, *kw)
  return wrapped

def executor_function(sync_function):
  @functools.wraps(sync_function)
  async def sync_wrapper(*args, **kw):
    #loop = asyncio.get_event_loop()
    #return await loop.run_in_executor(None, functools.partial(sync_function, *args, **kw))
    return await asyncio.get_event_loop().run_in_executor(None, functools.partial(sync_function, *args, **kw))
  return sync_wrapper

def executor(function):
  @wraps(function)
  def decorator(loop, *args, **kw):
    loop = loop or asyncio.get_event_loop()
    return loop.run_in_executor(None, function, *args, **kw)
    #return await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
  return decorator

'''
https://github.com/RobertCDR/Kanemki/blob/main/cogs/mod.py
https://github.com/RobertCDR/Kanemki/blob/main/cogs/utils.py
https://github.com/RobertCDR/Kanemki/blob/main/bot.py


https://github.com/Rapptz/discord.py/discussions/5877
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/converter.py

@commands.guild_only()
'''
  