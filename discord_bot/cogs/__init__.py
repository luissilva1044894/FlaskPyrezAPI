#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class ExtendedEmbed(discord.Embed):
  """An extended discord.Embed class"""
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.set_footer(text='', icon_url='')

class BaseCog(commands.Cog, name='Example'):
  def __init__(self, bot):
    self.bot = bot
  def codeblock(s, lang=None):
    if lang:
        return f'```{lang}\n{s}```'
    return f'```{s}```'
  @staticmethod
  def load_json(filename):
    """Loads a json file"""
    import json
    with open(filename, encoding='utf-8') as f:
        return json.load(f)
  @staticmethod
  def write_json(filename, contents):
    """Updates a json file"""
    with open(filename, 'w') as f:
        json.dump(contents, f, ensure_ascii=True, indent=4)
  @staticmethod
  def root(*chunks, root_='..'):
    import os#.path
    return os.path.abspath(os.path.join(os.path.dirname(__file__), root_, *chunks))
  @staticmethod
  def check_disabled():
    def predicate(ctx):
      if command_is_disabled(ctx.command.name, ctx.channel.id):
        raise DisabledInChannel('{ctx.command.name} is disabled in {ctx.channel.name}'.format(ctx=ctx))
      return True
    return commands.check(predicate)
  @staticmethod
  def isAuthorized():
    async def predicate(ctx):
        return ctx.bot.isAuthorized(ctx)
    return commands.check(predicate)
  @staticmethod
  def isMod():
    async def predicate(ctx):
        return ctx.bot.isMod(ctx)# or ctx.bot.isOwner(ctx)
    return commands.check(predicate)
  @staticmethod
  async def mark_check(ctx, mark=None):
    await ctx.message.add_reaction(mark or '✅')
  @staticmethod
  async def mark_check_no(ctx, *, mark=None):
    await BaseCog.mark_check(ctx, mark or '🚫')
  @staticmethod
  async def positive_reply(ctx, msg, *, mark=None):
    await BaseCog.mark_check(ctx, mark)
    await ctx.send(msg)
  @staticmethod
  async def negative_reply(ctx, msg, *, mark=None):
    await BaseCog.mark_check_no(ctx, mark)
    await ctx.send(msg)
  async def dl_image(self, url: str):
    async with self.session.get(str(url)) as resp:
        if resp.status == 200:
            test = await resp.read()
            return BytesIO(test)
        else:
            return None
