#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

