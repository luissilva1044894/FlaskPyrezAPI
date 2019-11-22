import random
import discord
import json

from discord.ext import commands
from discord import File

lenny_hug = [ "(つ ♡ ͜ʖ ♡)つ", "ლ(▀̿Ĺ̯▀̿ ̿ლ)", "(づ ͡° ³ ͡°)づ", "(つ ♥灬 ͜ʖ 灬♥)つ", "(つ ͡° ͜ʖ ͡°)つ",
  "c⌒っ ͡° ͜ʖ ͡°)っ", "d=( ͡° ͜ʖ ͡°)=b", "( ˶˘ ³˘(˵ ͡° ͜ʖ ͡°˵)♡", "( ͡° ▽ ͡°)爻( ͡° ل͜ ͡° ☆)", "(Ɔ ͡° ل͜ ͡°)(˘⌣˘) ͡° ل͜ ͡° C)",
  "(つ ♥ ͜ʖ ♥)つ", "⊂(▀̿Ĺ̯▀̿ ̿⊂)⊂( ͡° ͜ʖ ͡°)⊃", "(つ 灬♥ ͜ʖ ♥灬)つ", "★⌒ヽ( ͡° ε ͡°)", "(つ ͡ꈍ ͜ʖ̫ ͡ꈍ )つ", "(* ͡° ͜ʖ ͡°)(-*)ゝ",
  "*♡+( ͡° ل͜ ͡°)ε｀*)+♡*", "ヽ༼ ຈل͜ຈ༼ ▀̿̿Ĺ̯̿̿▀̿ ̿༽Ɵ͆ل͜Ɵ͆ ༽ﾉ" ]

class Hug(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(name="hug", description="Da un abrazo", brief="Abrazos everywhere",)
  async def hug(self, ctx, *, member: discord.Member = None):
    try:
        if member is None:
            await ctx.send("¡Ten un abrazo {}! \\ ( ͡° ͜ʖ ͡°) /".format(ctx.message.author.mention))
        else:
            if member.id == ctx.message.author.id:
                await ctx.send(file=File("{}forever_alone.png".format(memes_dir)),content="¡{} se ha abrazado a si mismo! ~~forever alone~~".format(ctx.message.author.mention),)
            else:
                await ctx.send("¡{} ha sido abrazado por {}! {}".format(member.mention,ctx.message.author.mention,random.choice(lenny_hug),))
        # print(member.avatar_url, ctx.message.author.avatar_url)
    except Exception as e:
        exc = "{}: {}".format(type(e).__name__, e)
        await ctx.send("{}".format(exc))
def setup(client):
  client.add_cog(Hug(client))
