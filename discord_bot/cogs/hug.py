import random
import discord
import json

from discord.ext import commands
from discord import File

lenny_hug = [ '(つ ♡ ͜ʖ ♡)つ', 'ლ(▀̿Ĺ̯▀̿ ̿ლ)', '(づ ͡° ³ ͡°)づ'  ]

class Hug(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='hug', description='Da un abrazo', brief='Abrazos everywhere',)
  async def hug(self, ctx, *, member: discord.Member = None):
    try:
        if member is None:
            await ctx.send('¡Ten un abrazo {}! \\ ( ͡° ͜ʖ ͡°) /'.format(ctx.message.author.mention))
        else:
            if member.id == ctx.message.author.id:
                await ctx.send(file=File(f'{memes_dir}forever_alone.png'),content='¡{} se ha abrazado a si mismo! ~~forever alone~~'.format(ctx.message.author.mention),)
            else:
                await ctx.send('¡{} ha sido abrazado por {}! {}'.format(member.mention,ctx.message.author.mention,random.choice(lenny_hug),))
        # print(member.avatar_url, ctx.message.author.avatar_url)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(f'{exc}')
def setup(bot):
  bot.add_cog(Hug(bot))
