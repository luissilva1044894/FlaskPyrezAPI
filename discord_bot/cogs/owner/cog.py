#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

def is_not_me():
  async def predicate(ctx):
    return ctx.message.content.lower().replace('cogs.', '').rfind('{} {}'.format(ctx.command.name.lower(), 'owner')) == -1
  return commands.check(predicate)

from ..__init__ import BaseCog
class Cog(BaseCog, name='Owner'):
    """Owner-only commands used to maintain the bot."""
    def __init__(self, bot):
        self.bot = bot
        #print(await bot.application_info())
    @staticmethod
    def fix_extension_name(ext_name):
      if ext_name.startswith('cogs.'):
        return ext_name.lower()
      return 'cogs.{}'.format(ext_name).lower()

    @commands.command(no_pm=True)
    #@BaseCog.isOwner()
    async def set_status(self, ctx, *, terms):
        """Change the bot status (Owner only)"""
        await self.bot.change_presence(status=discord.Status.online, activity=discord.activity.Game(name=terms))
    #@commands.command(description='')
    #@commands.is_owner()
    #async def restart(self, ctx):
    #    def stop_and_restart():
    #        """Gracefully stop the bot and replace the current process with a new one"""
    #        os.execl(sys.executable, sys.executable, *sys.argv)
    #    import sys
    #    import os
    #    from threading import Thread
    #    Thread(target=stop_and_restart).start()
    #    await self.mark_check(ctx)
    @commands.command(description='')
    @commands.is_owner()
    async def logout(self, ctx):
        """Logs out of the bot (Owner only)"""
        #if ctx.message.author.id == habchy:
        await self.mark_check(ctx)
        await ctx.send("👋 **Goodbye!**")
        await self.bot.change_presence(activity=discord.Game(name=''), status=discord.Status('offline'))
        await self.bot.logout()
        #else: await self.mark_check_no(ctx)

    @commands.command(description='')
    @commands.is_owner()
    async def leave(self, ctx, *, guild_name):
        """Leaves a guild (Owner only)"""
        guild = discord.utils.get(self.bot.guilds, name=guild_name)
        if guild:
          await self.bot.leave_guild(guild)
          await self.mark_check(ctx)
          await ctx.send(f':ok_hand: Left guild: {guild.name} ({guild.id})')
        else:
          await self.mark_check_no(ctx)
          await ctx.send("I don't recognize that guild.")
    
    # Hidden means it won't show up on the default help.
    @commands.command(description='', name='load', hidden=True)
    @commands.is_owner()
    @is_not_me()
    async def load(self, ctx, *, extension_name):
        """Command which Loads a Module (Owner only)."""
        try:
            self.bot.load_extension(self.fix_extension_name(extension_name))
        except (AttributeError, ImportError, commands.errors.ExtensionNotLoaded, commands.errors.CheckFailure) as e:
            await self.mark_check_no(ctx)
            await ctx.send("**`ERROR:`**\n\n```py\n{}: {}\n```".format(type(e).__name__, str(e))) #bot.say
        else:
            await self.mark_check(ctx)
            await ctx.send('**`SUCCESS`**: {} module loaded.'.format(extension_name))
    @commands.command(description='', name='unload', hidden=True)
    @commands.is_owner()
    @is_not_me()
    async def unload(self, ctx, *, extension_name):
        """Command which Unloads a Module (Owner only)."""
        try:
            self.bot.unload_extension(self.fix_extension_name(extension_name))
        except (AttributeError, ImportError, commands.errors.ExtensionNotLoaded, commands.errors.CheckFailure) as e:
            await self.mark_check_no(ctx)
            await ctx.send("**`ERROR:`**\n\n```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        else:
            await self.mark_check(ctx)
            await ctx.send('**`SUCCESS`**: {} module unloaded.'.format(extension_name))
    @commands.command(no_pm=True)
    #@BaseCog.isOwner()
    async def config(self, ctx):
      """Post the current config file in the debug channel (Owner only)"""
      try:
        with open('config.json', 'r') as f:
          await ctx.send('config.json', file=discord.File(f))
      except Exception as e:
        await self.mark_check_no(ctx)
      else:
        await self.mark_check(ctx)
    @commands.command()
    async def set_name(self, ctx, *, name):
      """Sets the bot's name (Owner only)."""
      try:
        await ctx.bot.user.edit(username=name)
      except Exception as e:
        await ctx.send(e)
      else:
        await ctx.send(f'Name set to {name}.')
    @commands.command()
    async def setavatar(self, link):
      """Sets the bot's avatar (Owner only)."""
      async with self.bot.session.get(link) as r:
        if r.status == 200:
          try:
            await self.bot.user.edit(avatar=await r.read())
          except Exception as e:
            await self.bot.send(e)
          else:
            await self.bot.send('Avatar set.')
        else:
          await self.bot.send('Unable to download image.')
    @commands.command(description='', name='reload', hidden=True)#pass_context=True, 
    @commands.is_owner()
    @is_not_me()
    async def reload(self, ctx, *, extension_name):
        """Command which Reloads a Module (Owner only)."""
        try:
            #print(extension_name.lower() == self.__class__.__name__.replace('Cog', '').lower())
            #print(self.__class__.__name__.replace('Cog', '').lower())
            #print(extension_name.lower())
            #self.bot.unload_extension(self.fix_extension_name(extension_name))
            #self.bot.load_extension(self.fix_extension_name(extension_name))
            self.bot.reload_extension(self.fix_extension_name(extension_name))
        except (AttributeError, ImportError, commands.errors.ExtensionNotLoaded, commands.errors.CheckFailure) as e:#Exception
            await self.mark_check_no(ctx)
            await ctx.send("**`ERROR:`**\n\n```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        else:
            await self.mark_check(ctx)
            await ctx.send('**`SUCCESS`**: {} module loaded.'.format(extension_name))
