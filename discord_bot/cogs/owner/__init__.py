#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

def setup(bot):
	from .cog import Cog
	bot.add_cog(Cog(bot))
