#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from utils.discord.helpers import get_aliases
class ExtendedEmbed(discord.Embed):
  """An extended discord.Embed class"""
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.set_footer(text='', icon_url='')
class Cog(commands.Cog, name='Example'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def ping(self, ctx, *args):
    import asyncio
    from datetime import datetime

    await ctx.send(':ping_pong:')
    latency=str(round(self.bot.latency*1000, 2))
    embed=discord.Embed(title='', colour=0x7289da, timestamp=datetime.utcnow())
    embed.set_author(name='Pong!')
    embed.add_field(name='Bot latency', value=f'{latency} ms')
    await ctx.send(embed=embed)

    await asyncio.sleep(3)
    await ctx.send(':warning:')

  @commands.command(description='')
  @commands.guild_only()
  async def joined(self, ctx, *, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.display_name} joined on {member.joined_at}')

  @commands.command(description='', name='coolbot', usage='<text>')
  async def cool_bot(self, ctx):
    """Is the bot cool?"""
    await ctx.send('This bot is cool. :)')
  @commands.command(description='', name='top_role', aliases=get_aliases('show_toprole'))
  @commands.guild_only()
  async def show_toprole(self, ctx, *, member=None):
    """Simple command which shows the members Top Role."""
    if member is None:
      member = ctx.author
    await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')

  @commands.command(description='', name='perms', aliases=get_aliases(['perms_for', 'permissions']))
  @commands.guild_only()
  async def check_permissions(self, ctx, *, member=None):
    """A simple command which checks a members Guild Permissions.
    If member is not provided, the author will be checked."""

    if not member:
      member = ctx.author
    # Here we check if the value of each permission is True.
    perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

    # And to make it look nice, we wrap it in an Embed.
    embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
    embed.set_author(icon_url=member.avatar_url, name=str(member))

    # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
    embed.add_field(name='\uFEFF', value=perms)

    await ctx.send(content=None, embed=embed)
    # Thanks to Gio for the Command.
