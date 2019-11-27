
import json
from discord.ext import commands
class WebSocket(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
