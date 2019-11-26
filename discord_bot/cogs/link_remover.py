

import discord

def cmd_enabled(guild_id):
  if isinstance(guild_id, int):
    return guild_id == 554372822739189761
  if hasattr(guild_id, 'id'):
    return cmd_enabled(guild_id.id)
  return False

class LinkRemover(discord.ext.commands.Cog, name='Link Remover'):
  """A cog for removing links, such as discord invites."""
  def __init__(self, bot):
    self.bot = bot
    self.invite_links = [ 'discord.gg', 'discordapp.com/invite', ]# any other popular invite link here

  @discord.ext.commands.Cog.listener()
  async def on_message(self, message):
    # bots, DMs and servers other than this one and bot owner are unaffected
    if message.author.bot or not message.guild or not cmd_enabled(message.guild.id) or message.author.id == self.bot.owner_id:
      return
    # detect and delete the message if necessary
    if (_ for _ in self.invite_links if _ in message.content):
      await message.delete()
      await message.channel.send('Smh, don\'t do that!')
    '''
    for link in self.invite_links:
      if link in message.content:
        await message.delete()
        await message.channel.send("Smh, don't do that!")
        break
    '''
def setup(bot):
  bot.add_cog(LinkRemover(bot))
