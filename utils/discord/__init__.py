#!/usr/bin/env python
# -*- coding: utf-8 -*-

async def get_background(self, url, session):
	from io import BytesIO
	from PIL import Image
	async with session.get(url) as f:
		return Image.open(BytesIO(await f.read()))

async def get_avatar(self, user, session, *, format='png', size=1024):
	from io import BytesIO
	try:
		res = BytesIO()
		await user.avatar_url_as(format=format, size=size).save(res, seek_begin=True)
		return res
	except:
		async with session.get(user.avatar_url_as(format=format, size=size)) as r:
			return BytesIO(await r.content.read())

class DiscordConfig(object):
	"""
	docstring for DiscordConfig

	from config import DiscordConfig
	x = DiscordConfig()
	print(x['token'])
	print(x.get('token'))
	print(x.token)
	print(x)
	"""
	def __init__(self, *, _config='data/config.json'):
		#./../config/config.json
		self.load(_config)
	def load(self, path):
		import os
		if not os.path.isfile(path):#os.path.isdir(path)
			path = join(path, 'config.json')
		from utils.file import read_file
		self.__kwargs__ = read_file(path, is_json=True)
	def get(self, key, default=None):
		return self.__getitem__(key) or default
	def __getitem__(self, key):
		try:
			return self.__kwargs__[key]
		except KeyError:
			return None
	def __contains__(self, key):
		return key in self.__kwargs__
	def __dir__(self):
		if isinstance(self.__kwargs__, dict):
			return self.__kwargs__.keys()
		return {}
	def __len__(self):
		return len(self.__kwargs__)
	def __iter__(self):
		return (key for key in self.__kwargs__) #return (self.__kwargs__[key] for key in self.__kwargs__)
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		if self.__kwargs__:
			import json
			return json.dumps(self.__kwargs__, ensure_ascii=True, sort_keys=True, indent=2)
		return ''

def load_cogs(bot, cogs_dir='cogs'):
	"""Automagically register all cogs packages inside a 'cogs' folder."""
	from os import listdir, getcwd
	from os.path import isfile, join, isdir
	for _ in listdir('.'):
		if isdir(_) and not _.startswith('_') and not _.startswith('.'):
			try:
				for __ in listdir(join(getcwd(), _, cogs_dir)):#'./cogs'
					if not __.startswith('__'):
						try:
							if __.endswith('.py'):
								bot.load_extension(f'{_}.{cogs_dir}.{__[:-3]}')
							else:
								bot.load_extension('.'.join([_, cogs_dir, __]))
							print(f'>>> Loaded extension: { __}')
						except Exception as e:#(commands.errors.ExtensionNotFound, commands.errors.NoEntryPointError) as e:
							exc = '{}: {}'.format(type(e).__name__, e)
							print(f'Failed to load extension {__}\n{exc}')#, file=sys.stderr)
			except FileNotFoundError:
				pass

