#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from discord.ext import commands
import json

from web.models.paladins.player import Player
from boolify import boolify
class Bot(commands.Bot):
	def __init__(self, *, config=None, import_name=None, command_prefix=None, **kwargs):
		from utils import get_root_path
		from utils.config import Config
		self.root_path = get_root_path(kwargs.pop('import_name', None) or __name__)
		#from wsgi import app
		#Player(id=123, name='Nonsocial', platform='PC')
		#input(Player.query.all())
		self.config = Config(self.root_path)

		debug = kwargs.pop('debug', None)
		if debug: self.debug = boolify(debug)
		self.token = kwargs.pop('token', None)

		self.prefixes = {}
		from utils.discord.helpers import _prefix_callable
		super().__init__(command_prefix=command_prefix or _prefix_callable)
		self.initialised = False
		self.session = None  # Async init
	async def aio(self, method, url, return_attr, **kwargs):
		async with self.session.request(method, url, **kwargs) as r:
			if not return_attr:
				return r
			return r, await getattr(r, return_attr)()
	async def close(self):
		if self.session:
			await self.session.close()
		await super().close()
	async def on_connect(self):
		self.remove_command('help')
	async def on_ready(self):
		if not hasattr(self, 'app_info'):
			self.app_info = await self.application_info()
		if not hasattr(self, 'start_time'):
			from datetime import datetime
			self.start_time = datetime.utcnow()
		from utils.discord import load_cogs
		load_cogs(self)
		if not self.initialised:
			import aiohttp
			import discord
			self.session = aiohttp.ClientSession(loop=self.loop)
			from datetime import datetime
			self.initialised = True
			await self.change_presence(activity=discord.Game(name='Paladins'), status=discord.Status('dnd')) #This is buggy, let us know if it doesn't work.
			#await self.change_presence(activity=discord.Activity(name="my meat", type=3))
			#self.loop.create_task(change_bot_presence_task())
			print(f'\nTotal Startup: {datetime.utcnow() - self.start_time}', end='\n')
		import platform
		print('=' * 75, end='\n\n')
		print(f'Logged in as: {self.user.name} - ID: {self.user.id}\nConnected to {len(self.guilds)} servers | Connected to {len(set(self.get_all_members()))} users', end='\n')
		print(f'\nDiscord.py: v{discord.__version__} | Python: v{platform.python_version()}', end='\n')
		print(f'\nUse this link to invite {self.user.name}:\nhttps://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=8', end='\n')
		print(f'\nSupport Discord Server: {self.dev_server}\nGithub repo: {self.github_repo}', end='\n')
		print(f'\nCreated by {self.app_info.owner}', end='\n')
		print(f'Successfully logged in and booted...!', end='\n\n')
		print('=' * 75, end='\n\n')
	@property
	def dev_server(self):
		return self.config['DEV_SERVER']
	@property
	def github_repo(self):
		return self.config['GITHUB_REPO']
	@property
	def uptime(self):
		from datetime import datetime
		delta = datetime.now() - self.start_time#int(datetime.now().timestamp()) - self.db.get('start_time')
		return delta#time.human_time(delta.total_seconds())
	'''
	async def on_message(self, message):
		# don't respond to ourselves
		if message.author == self.user or message.author.bot:
			return
	'''
	def run(self, *args, **kwargs):
		# debug passed to method overrides all other sources
		debug, token = kwargs.pop('debug', None), kwargs.pop('token', None)
		if debug: self.debug = boolify(debug)
		if token: self.token = token
		super().run(*args or (self.token,), **kwargs)
	@property
	def debug(self):
		return self.config.get('DEBUG', False)
	@debug.setter
	def debug(self, value):
		self.config['DEBUG'] = value
	@property
	def token(self):
		return self.config.get('TOKEN') or None
	@token.setter
	def token(self, value):
		if value:
			self.config['TOKEN'] = value
