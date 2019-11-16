#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

def isNotMe():
    async def predicate(ctx):
        return ctx.message.content.lower().replace('cogs.', '').rfind('{} {}'.format(ctx.command.name.lower(), 'owner')) == -1
    return commands.check(predicate)

from ..__init__ import BaseCog
class Cog(BaseCog, name='Owner'):
    def __init__(self, bot):
        self.bot = bot
        #print(await bot.application_info())
    @staticmethod
    def fix_extension_name(extension_name):
        if extension_name.startswith('cogs.'):
            return extension_name.lower()
        return 'cogs.{}'.format(extension_name).lower()

    @commands.command(no_pm=True)
    @BaseCog.isOwner()
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
        """Make the bot quit"""
        #if ctx.message.author.id == habchy:
        await self.mark_check(ctx)
        await ctx.send("👋 **Goodbye!**")
        await self.bot.change_presence(activity=discord.Game(name=''), status=discord.Status('offline'))
        await self.bot.logout()
        #else: await self.mark_check_no(ctx)

    @commands.command(description='')
    @commands.is_owner()
    async def leave(self, ctx, *, guild_name):
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
    @isNotMe()
    async def load(self, ctx, *, extension_name):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
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
    @isNotMe()
    async def unload(self, ctx, *, extension_name):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.unload_extension(self.fix_extension_name(extension_name))
        except (AttributeError, ImportError, commands.errors.ExtensionNotLoaded, commands.errors.CheckFailure) as e:
            await self.mark_check_no(ctx)
            await ctx.send("**`ERROR:`**\n\n```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        else:
            await self.mark_check(ctx)
            await ctx.send('**`SUCCESS`**: {} module unloaded.'.format(extension_name))
    @commands.command(no_pm=True)
    @BaseCog.isOwner()
    async def config(self, ctx):
        """Post the current config file in the debug channel (Owner only)"""
        try:
            with open('config.json', 'r') as infile:
                await ctx.send('config.json', file=discord.File(infile))
        except Exception as e:
            await self.mark_check_no(ctx)
        else:
            await self.mark_check(ctx)
    @commands.command(description='', name='reload', hidden=True)#pass_context=True, 
    @commands.is_owner()
    @isNotMe()
    async def reload(self, ctx, *, extension_name):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
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
