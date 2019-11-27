#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

def setup(bot):
	from utils import on_heroku
	if on_heroku():
		from .websocket_client import WebSocket
		w = WebSocket(bot)
	else:
		from .websocket_server import WebSocket
		import asyncio
		import websockets
		w = WebSocket(bot)
		try:
			asyncio.get_event_loop().run_until_complete(websockets.serve(w.websocket_listener, 'localhost', 8785))
		except RuntimeError:
			pass
	bot.add_cog(w)
