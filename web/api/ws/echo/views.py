#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import is_async
if is_async():
	from utils.web import create_blueprint
	blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', template_folder='templates', url_prefix='/{}'.format('/'.join(__name__.split('.')[1:-1])))

	from quart import websocket
	import asyncio

	@blueprint.route('/', strict_slashes=False)
	async def index():
		"""https://medium.com/@pgjones/websockets-in-quart-f2067788d1ee"""
		from quart import render_template
		return await render_template('{}/index.html'.format(__name__.split('.')[-3]))

	def auth_required(func):
		from functools import partial, wraps
		from quart import abort, current_app, websocket

		@wraps(func)
		async def wrapper(*args, **kwargs):
			auth = websocket.authorization
			#from secrets import compare_digest
			#if auth and auth.username == current.app.config['USERNAME'] and compare_digest(auth.password, current.app.config['PASSWORD'],):
			#	return await func(*args, **kwargs)
			if auth:
				return await func(*args, **kwargs)
			abort(401)
		return wrapper

	@blueprint.websocket('/', strict_slashes=False)
	#@auth_required
	async def __echo__():
		"""https://medium.com/@pgjones/websockets-in-quart-f2067788d1ee"""
		try:
			await websocket.send('Connected!')
			while True:
				#await websocket.send(b'spam')
				#await asyncio.sleep(10)
				data = await websocket.receive()
				if data:
					await websocket.send(f'echo {data}')
		except asyncio.CancelledError:
			print('Client disconnected')
