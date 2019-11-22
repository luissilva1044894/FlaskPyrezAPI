#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

#A list of all special cog methods: https://gist.github.com/Ikusaba-san/69115b79d33e05ed07ec4a4f14db83b1
# https://gitlab.giesela.ch/shikhirarora/Discord-Selfbot/tree/master
# https://gitlab.giesela.ch/shikhirarora/Discord-Selfbot/blob/master/appuselfbot.py
# https://stackoverflow.com/questions/56380783/discord-py-rewrite-music-cannot-use-check

# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case ExampleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
  """Adds the cog to the bot (Required). You can do whatever you want here. Most common usage is to simply add the cog.
  Note: The "setup" function has to be there in every cog file
  """
  from .cog import Cog
  bot.add_cog(Cog(bot))
def teardown(bot):
  """Optional. Cogs automatically get removed regardless of whether or not this is here."""
  pass
