
import json
from discord.ext import commands
class WebSocket(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
  def build_bot_json(self):
    '''
    __cogs__, cogs_desc = [], ''
    __cogs_commands__ = []
    __commands__ = []
    for y in self.bot.walk_commands():
      if not y.cog_name and not y.hidden:
        __commands__.append('{} - {}'.format(y.name,y.help)+'\n')
      else:
        __cogs_commands__.append('{} - {}'.format(y.name,y.help)+'\n')
    print(__cogs_commands__)
    for x in self.bot.cogs:
      #cogs_desc += ('{} - {}'.format(x, self.bot.cogs[x].__doc__)+'\n')
      
      #cogs_desc = ('{} - {}'.format(x, self.bot.cogs[x].__doc__)+'\n')
      #__cogs__.append(cogs_desc[0:len(cogs_desc)-1])
      __cogs__.append(('{} - {}'.format(x, self.bot.cogs[x].__doc__)+'\n'))
      #cogs_desc = ''
    '''

    '''
    for x in self.bot.cogs:
      __cmds__ = ''
      for y in self.bot.walk_commands():
        if x == y:
          __cmds__ += f'{y} - {y.help}\n\n'
      __cogs__.append(f'{x} - {self.bot.cogs[x].__doc__}\n{__cmds__}\n')
    '''
    return {
      'connection': {
        'user': { 'name': str(self.bot.user) },
        '_servers': [str(g) for g in self.bot.guilds]
      },
      'config': self.bot.config,
      #'cogs': ['{} - {}\n{}'.format(str(x), self.bot.cogs[x].__doc__, '<br/>'.join(f'{y.name} - {y.help}' for y in self.bot.get_cog(x).get_commands())) for x in self.bot.cogs],
      'cogs': [ { 'name': x, 'doc': self.bot.cogs[x].__doc__, 'cmds': [f'{y.name} - {y.help}' for y in self.bot.get_cog(x).get_commands()] } for x in self.bot.cogs if x != self.__class__.__name__ ],
      #'cogs': [(f'{x} - {self.bot.cogs[x].__doc__}\n') for x in self.bot.cogs],
      #'cogs': [type(c).__name__ for c in self.bot.cogs.values()],
      #'commands': {str(c): c.help for c in self.bot.commands},
      'commands': { str(c): c.help for c in self.bot.walk_commands() if not c.cog_name },#and not y.hidden #__commands__,
      'settings': {
        'bot_settings': {
          'PREFIXES': {'0': str('TODO')},
          'default': {
            'ADMIN_ROLE': str('TODO: Remove this'),
            'MOD_ROLE': str('TODO: Remove this')
          }
        }
      },
      '_is_logged_in': { '_value': str('TODO: Remove this') }
    }
  async def websocket_listener(self, websocket, path):
    msg = await websocket.recv()
    if msg == 'list_info':  # first contact
      await websocket.send(json.dumps(self.build_bot_json(), indent=2))

def setup(bot):
	import asyncio
	import websockets

	w = WebSocket(bot)
	try:
		asyncio.get_event_loop().run_until_complete(websockets.serve(w.websocket_listener, 'localhost', 8785))
	except RuntimeError:
		pass
	bot.add_cog(w)

"""
{
  "connection": {
    "user": {
      "name": "nonsocial-bot#8586"
    },
    "_servers": [
      "n-s"
    ]
  },
  "config": {
    "DATABASE_URI": "sqlite:///web.db",
    "DEBUG": true,
    "DEVELOPMENT": true,
    "DEV_SERVER": "https://discord.gg/XkydRPS",
    "GITHUB_REPO": "https://github.com/luissilva1044894/FlaskPyrezAPI",
    "ON_HEROKU": false,
    "PREFIXES": [
      "?",
      "!",
      ">",
      "$"
    ],
    "SECRET_KEY": "testkey",
    "SQLALCHEMY_BINDS": {
      "database": "sqlite:///database.db",
      "paladins": "sqlite:///paladins.db",
      "smite": "sqlite:///smite.db",
      "discord": "sqlite:///discord.db"
    },
    "SQLALCHEMY_DATABASE_URI": "sqlite:///web.db",
    "SQLALCHEMY_TRACK_MODIFICATIONS": false,
    "TESTING": true,
    "TOKEN": "NDU3NjAwMTk3MzY3OTU1NDg2.Dgbfnw.wrUCcZzRBFaavAkT4ieqR_-uus4"
  },
  "cogs": [
    {
      "name": "Example",
      "doc": null,
      "cmds": [
        "ping - None",
        "joined - Says when a member joined.",
        "coolbot - Is the bot cool?",
        "top_role - Simple command which shows the members Top Role.",
        "perms - A simple command which checks a members Guild Permissions.\nIf member is not provided, the author will be checked."
      ]
    },
    {
      "name": "Hug",
      "doc": null,
      "cmds": [
        "hug - None"
      ]
    },
    {
      "name": "LinkRemover",
      "doc": "A cog for removing links, such as discord invites.",
      "cmds": []
    },
    {
      "name": "Owner",
      "doc": "Owner-only commands used to maintain the bot.",
      "cmds": [
        "set_status - Change the bot status (Owner only)",
        "logout - Logs out of the bot (Owner only)",
        "leave - Leaves a guild (Owner only)",
        "load - Command which Loads a Module (Owner only).",
        "unload - Command which Unloads a Module (Owner only).",
        "config - Post the current config file in the debug channel (Owner only)",
        "set_name - Sets the bot's name (Owner only).",
        "setavatar - Sets the bot's avatar (Owner only).",
        "reload - Command which Reloads a Module (Owner only)."
      ]
    },
    {
      "name": "Server Owner",
      "doc": null,
      "cmds": [
        "prefix - prefix [prefix]"
      ]
    },
    {
      "name": "WebSocket",
      "doc": null,
      "cmds": []
    }
  ],
  "commands": {},
  "settings": {
    "bot_settings": {
      "PREFIXES": {
        "0": "TODO"
      },
      "default": {
        "ADMIN_ROLE": "TODO: Remove this",
        "MOD_ROLE": "TODO: Remove this"
      }
    }
  },
  "_is_logged_in": {
    "_value": "TODO: Remove this"
  }
}
"""