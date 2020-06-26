#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime
from os import environ
import json
import platform
from traceback import TracebackException

import aiohttp
from boolify import boolify
import discord
from discord.ext import commands

from config import get_config
from utils.discord import load_cogs

class Bot(commands.Bot):
  def __init__(self, *, config=None, import_name=None, command_prefix=None, pm_help=False, **kw):
    if not hasattr(self, 'start_time'):
      self.start_time = datetime.utcnow()

    debug = kw.pop('debug', None)
    self.token = kw.pop('token', None)

    if self.token and not config:
      self.config = get_config('discord')

    self.prefixes = {}
    super().__init__(command_prefix=command_prefix or '!', pm_help=pm_help, **kw)
    self.initialised = False
    self.session = None  # Async init
  async def aio_request(self, method, url, return_attr, **kw):
    async with self.session.request(method, url, **kw) as r:
      if not return_attr:
        return r
      return r, await getattr(r, return_attr)()
  async def close(self):
    if self.session:
      await self.session.close()
    for _ in asyncio.all_tasks(loop=self.loop):
      _.cancel()
    #await self.logout() #close / logout loop
    await super().close()
  async def on_connect(self):
    self.remove_command('help')
    load_cogs(self)
  async def on_ready(self):
    if not hasattr(self, 'app_info'):
      self.app_info = await self.application_info()
    if not self.initialised:
      self.session = aiohttp.ClientSession(loop=self.loop)
      self.initialised = True
      await self.change_presence(activity=discord.Game(name='Paladins'), status=discord.Status('dnd'))
      print(f'\nTotal Startup: {self.uptime}', end='\n')
    print('=' * 75, end='\n')
    print(f'Logged in as: {self.user.name} (ID:{self.user.id})\r\nConnected to {len(self.guilds)} servers | Connected to {len(set(self.get_all_members()))} users')
    print(f'https://discordapp.com/oauth2/authorize?client_id={self.user.name}&scope=bot&permissions=8')
    print(f'Successfully logged in and booted...!')
    print('=' * 75, end='\n\n')
  def run(self, *args, **kwargs):
    """debug passed to method overrides all other sources"""
    debug, token, reconnect = kwargs.pop('debug', None), kwargs.pop('token', None), kwargs.pop('reconnect', True)
    if debug:
      self.debug = boolify(debug)
    if token:
      self.token = token
    super().run(*args or (self.token,), reconnect=reconnect, **kwargs)
  @property
  def owner(self):
    if hasattr(self, 'app_info'):
      return self.app_info.owner#.id
  @property
  def ping(self):
    return f'{round(self.latency * 1000)}ms'
  @property
  def timestamp(self):
    return datetime.utcnow()
  @property
  def uptime(self):
    return self.timestamp - self.start_time
