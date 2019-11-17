#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from discord.ext import commands
import json

class Bot(commands.Bot):
	def __init__(self, *, config=None, command_prefix=('!', '?')):
		super().__init__(command_prefix=command_prefix)
		self.config = config
		from utils.discord import load_cogs
		load_cogs(self)
	async def on_connect(self):
		pass
	async def on_ready(self):
		from discord import Activity
		#await self.change_presence(activity=Activity(name="my meat", type=3))
		if not hasattr(self, 'appinfo'):
			self.appinfo = await self.application_info()
		import platform
		import discord
		print(f'\n\nLogged in as: {self.user.name} - ID: {self.user.id}\nConnected to {len(self.guilds)} servers | Connected to {len(set(self.get_all_members()))} users', end='\n')
		print(f'\nDiscord.py: v{discord.__version__} | Python: v{platform.python_version()}', end='\n')
		print(f'\nUse this link to invite {self.user.name}:\nhttps://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=8', end='\n')
		print('\nSupport Discord Server: https://discord.gg/XkydRPS\nGithub Link: https://github.com/luissilva1044894/PyrezBot', end='\n')
		print(f'\nCreated by {self.appinfo.owner}', end='\n')
		#self.loop.create_task(change_bot_presence_task())
		from datetime import datetime
		self.start_time = datetime.utcnow()
		#from utils.discord import load_cogs
		#load_cogs(self)
		#Here we load our extensions(cogs) listed above in [initial_extensions]
		print(f'Successfully logged in and booted...!')
		return await self.change_presence(activity=discord.Game(name='Paladins'), status=discord.Status('dnd')) #This is buggy, let us know if it doesn't work.
	@property
	def uptime(self):
		from datetime import datetime
		return datetime.now() - self.start_time
		#return int(datetime.now().timestamp()) - self.db.get('start_time')
	async def on_message(self, message):
		# don't respond to ourselves
		if message.author == self.user:
			return
