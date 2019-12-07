
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
        'user': { 'id': self.bot.user.id, 'name': str(self.bot.user) },#.split('#', 1)[0]
        '_servers': [str(g) for g in self.bot.guilds]
      },
      'config': {_: self.bot.config[_] for _ in self.bot.config if _.lower().rfind('token') == -1 and _.lower().rfind('pyrez') == -1}, #self.bot.config,
      #'cogs': ['{} - {}\n{}'.format(str(x), self.bot.cogs[x].__doc__, '<br/>'.join(f'{y.name} - {y.help}' for y in self.bot.get_cog(x).get_commands())) for x in self.bot.cogs],
      'cogs': [ { 'name': x, 'doc': self.bot.cogs[x].__doc__, 'cmds': [f'{y.name} - {y.help}' for y in self.bot.get_cog(x).get_commands()] } for x in self.bot.cogs if x != self.__class__.__name__ ],
      #'cogs': [(f'{x} - {self.bot.cogs[x].__doc__}\n') for x in self.bot.cogs],
      #'cogs': [type(c).__name__ for c in self.bot.cogs.values()],
      #'commands': {str(c): c.help for c in self.bot.commands},
      'commands': { str(c): c.help for c in self.bot.walk_commands() if not c.cog_name },#and not y.hidden #__commands__,
      'settings': {
        'bot_settings': {
          'PREFIXES': self.bot['PREFIXES'],#{'0': str('TODO')},
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
