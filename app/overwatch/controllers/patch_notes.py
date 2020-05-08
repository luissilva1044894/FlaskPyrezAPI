#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://playoverwatch.com/pt-br/news/patch-notes/pc
#https://playoverwatch.com/en-us/news/patch-notes/pc
#https://playoverwatch.com/es-es/news/patch-notes/pc
#https://playoverwatch.com/es-mx/news/patch-notes/pc
#https://playoverwatch.com/pl-pl/news/patch-notes/pc

from ...utils import get_url
from bs4 import BeautifulSoup
from bs4.element import Tag
def patch_notes_func():
  def get_patch_note_id(page):
    if page:
      for _ in page.find_all(class_='patch-notes-patch') or []:
        if isinstance(_, Tag) and 'div' in _.name:
          _id = _.get('id')
          if _id:
            return _id
    return ''
  def get_patch_note_title(page):
    if page:
      for patch in page.find(class_='patch-notes-patch'):
        if hasattr(patch, 'children'):
          title = next(patch.children, None)
          if title:
            return str(title).strip()
    return 'Latest Overwatch Patch Notes'
  _page = BeautifulSoup(get_url('https://playoverwatch.com/en-us/news/patch-notes/pc'), features='html.parser')
  return f'{get_patch_note_title(_page)} - Click here to view all the patch notes: https://playoverwatch.com/en-us/news/patch-notes/pc#{get_patch_note_id(_page)}'
'''
"""Overwatch API url (unofficial)."""
api = "https://ow-api.com/"

@commands.command()
async def status(self, ctx):
  async def get_server_status(self):
    """Returns Overwatch servers status."""
    async with self.session.get('https://downdetector.com/status/overwatch/') as r:
      content = await r.read()
    page = BeautifulSoup(content, features="html.parser")
    status = page.find(class_="entry-title")
    return status.get_text()

  """Returns Overwatch servers status."""
  async with ctx.typing():
    embed = discord.Embed(title="Overwatch servers status", color=self.bot.color, timestamp=self.bot.timestamp,)
    embed.set_footer(text="Data taken from downdetector.com")
    try:
      embed.description = await self.bot.get_server_status()
    except Exception:
      embed.description = (f"[Overwatch Servers Status](https://downdetector.com/status/overwatch/)")
    await ctx.send(embed=embed)

@commands.command()
async def news(self, ctx):
  async def get_news(self):
    """Returns Overwatch news."""
    async with self.session.get('https://playoverwatch.com/en-us/news') as r:
      content = await r.read()
    page, titles, links, imgs = BeautifulSoup(content, features="html.parser"), [], [], []
    for title in page.find_all("h1", {"class": "Card-title"}):
      titles.append(title.get_text())
    for link in page.find_all("a", {"class": "CardLink"}, href=True)[:4]:
      links.append("https://playoverwatch.com" + link["href"])
    for img in page.find_all("div", {"class", "Card-thumbnail"})[:4]:
      imgs.append(img["style"].split("url(")[1][:-1])
    return [titles, links, imgs]

  """Returns the latest news about Overwatch."""
  async with ctx.typing():
    pages = []
    try:
      title, link, img = await self.bot.get_news()
    except Exception:
      embed = discord.Embed(
        title="Latest Overwatch News",
        description=f"[Click here to check out all the new Overwatch news.](https://playoverwatch.com/en-us/news)",
        color=self.bot.color,
      )
      embed.set_footer(text="Blizzard Entertainment")
      await ctx.send(embed=embed)
    else:
      for i in range(4):
        embed = discord.Embed(title=title[i], url=link[i], color=self.bot.color, timestamp=self.bot.timestamp,)
        embed.set_image(url=f"https:{img[i]}")
        embed.set_footer(text=f"Page {i+1}/{len(title)} - Blizzard Entertainment")
        pages.append(embed)
      await self.bot.paginator.Paginator(extras=pages).paginate(ctx)
'''
