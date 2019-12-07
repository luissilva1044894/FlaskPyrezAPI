
import json
from discord.ext import commands
class WebSocket(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
    self.bot.loop.create_task(self.websocket_listener())
  async def websocket_listener(self):
    await self.wait_until_ready()
    while not self.bot.is_closed():
      pass
  async def on_change_pr(self, new_pr):
    try:
      await self.change_presence(activity=discord.Game(new_pr))
    except Exception as e:
      pass
  '''
  async def on_close(self):
    for task in asyncio.all_tasks(loop=self.loop):
      task.cancel()
    await self.logout()
  '''
  async def on_give_guilds(self):
    return [{'id': g.id, 'name': g.name, 'url': f"{'https://pmcvariety.files.wordpress.com/2018/05/discord-logo.jpg?' if not str(g.icon_url) else str(g.icon_url)}"} for g in self.guilds]
  async def on_give_channels(self, g_id):
    return [{'name': chn.name, 'id': chn.id} for chn in self.get_guild(int(g_id)).text_channels]
  async def on_give_chat(self, chn_id, limit=100):
    try:
      chn = self.get_channel(int(chn_id))
      history = await chn.history(limit=limit).flatten()
    except discord.errors.Forbidden as e:
      pass
    else:
      self.con.send([{'author': m.author.display_name, 'content': m.content, 'at': m.created_at, 'link': str(m.author.avatar_url)} for m in history])
