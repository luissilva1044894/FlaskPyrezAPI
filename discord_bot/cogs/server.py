import discord
from discord.ext import commands

import json

from utils.discord.helpers import is_guild_owner, get_aliases

class Server(commands.Cog, name='Server Owner'):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(brief='Change the prefix for your server', aliases=get_aliases('prefix'))
  #@commands.check(is_guild_owner)
  @is_guild_owner()
  async def prefix(self, ctx, *, pre):
    """prefix [prefix]"""
    with open(r'prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = pre

    with open(r'prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'New prefix is `{pre}`')

def setup(bot):
  bot.add_cog(Server(bot))
