
def get_aliases(x):
  if isinstance(x, list):
    return x
  return []#[x]

def ignore_bots():
  from discord.ext import commands
  async def predicate(ctx):#bot,
    #message.author.bot
    return not (cxt.author == bot.user or ctx.author.bot)
  return commands.check(predicate)

def is_owner_or_admin():
  from discord.ext import commands
  async def predicate(ctx):
    return ctx.bot.isOwner(ctx)
  return commands.check(predicate)

def is_guild_owner():
  from discord.ext import commands
  async def predicate(ctx):
    #ctx.author.id == ctx.guild.owner.id
    return ctx.author == ctx.guild.owner #raise NotServerOwner('Only the server owner: ' + str(ctx.guild.owner) + ' can use this command')
  return commands.check(predicate)
  
def codeblock(s, lang=None):
  if lang:
    return f'```{lang}\n{s}```'
  return f'```{s}```'
#https://github.com/Harmon758/Harmonbot

def _prefix_callable(bot, msg):
  #return msg.author.name[0]

  """An empty string as the prefix always matches, enabling prefix-less command invocation.
  While this may be useful in DMs it should be avoided in servers,
  as it’s likely to cause performance issues and unintended command invocations."""

  if bot.config['DEBUG'] or not message.guild:
    # Don't use as prefix when in DMs, this is optional
    return '' #bot.command_prefix
  base = [f'<@!{bot.user.id}> ', f'<@{bot.user.id}> ' ] # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix
  base.extend(bot.prefixes.get(msg.guild.id, bot.config['PREFIXES']))
  return base
  '''
  try:
    return bot.guild_prefixes[bot.guild_ids.index(message.guild.id)]
  except ValueError:
    pass
  return bot.config['prefix']
  
  def get_prefix(bot, message):
    import discord
    with open(f'{data_path}/prefixes.json', 'r') as prefixes_file:
        all_prefixes = json.load(prefixes_file)
        if isinstance(message.channel, discord.DMChannel):
            return all_prefixes.get(str(message.channel.id), '!')
        return all_prefixes.get(str(message.guild.id), '!')
  #utils.file.create_file('prefixes')

  try:
    import os
    with open('{}/{}'.format(os.path.dirname(os.path.abspath(__file__)) + '\\server_configs', message.guild.id), 'r', encoding='utf-8') as f:
        print(f.read())
        default_prefixes = [f.read()]
        #if str(message.guild.id) in self.prefixes: return self.prefixes[message.guild.id] # retrieve the prefix used by the server
  except FileNotFoundError:
    pass
  #try:
  #	from utils.database.db_functions import guild_ids, guild_prefixes
  #    prefix = guild_prefixes[guild_ids.index(message.guild.id)]#https://github.com/RubenJ01/rewrite/blob/master/utils/database/db_functions.py
  #except ValueError:
  #    prefix = bot.config['prefix']
  else:
    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*default_prefixes)(bot, message)#when_mentioned(*default_prefixes)(bot, message)
  return default_prefixes
'''
def get_online_members(guild):
  import discord
  return [_ for _ in guild.server.members if _.status == discord.Status.online and not _.bot]
