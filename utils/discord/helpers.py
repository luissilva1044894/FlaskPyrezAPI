def codeblock(s, lang=None):
    if lang:
        return "```{}\n{}```".format(lang, s)
    return "```{}```".format(s)
#https://github.com/Harmon758/Harmonbot
def get_prefix(bot, message):
    with open(data_path + "/prefixes.json", 'r') as prefixes_file:
        all_prefixes = json.load(prefixes_file)
    if isinstance(message.channel, discord.DMChannel):
        prefixes = all_prefixes.get(str(message.channel.id), None)
    else:
        prefixes = all_prefixes.get(str(message.guild.id), None)
    return prefixes if prefixes else '!'

#utils.file.create_file('prefixes')

def get_prefix(bot, message):
    guild_id = message.guild.id
    try:
        index = guild_ids.index(guild_id)
        prefix = guild_prefixes[index]
    except ValueError:
        prefix = bot.config['prefix']
    if not message.guild:
        return bot.command_prefix
    return prefix

def _prefix_callable(bot, msg):
    base = [f'<@!{bot.user.id}> ', f'<@{bot.user.id}> ']
    if msg.guild is None:
        base.append('?').append('!')
    else:
        base.extend(bot.prefixes.get(msg.guild.id, ['?', '!']))
    return base

def get_prefix(bot, message):
    """An empty string as the prefix always matches, enabling prefix-less command invocation.
    While this may be useful in DMs it should be avoided in servers, as it’s likely to cause performance issues and unintended command invocations.
    """
    if DEBUG:
        return ''#REMOVE THIS
    default_prefixes = [ '!', '>', '$' ] ## sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix
    if not message.guild:
        return '' # Don't use as prefix when in DMs, this is optional
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

def get_online_members(guild):
    import discord
    return [_ for _ in guild.server.members if _.status == discord.Status.online and not _.bot]
