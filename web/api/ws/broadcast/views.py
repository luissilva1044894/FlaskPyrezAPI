#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import is_async
if False:#is_async():
	from utils.web import create_blueprint
	blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', template_folder='templates', url_prefix='/{}'.format('/'.join(__name__.split('.')[1:-1])))

	connected_websockets = set()

	from quart import websocket
	import asyncio

	connected_websockets = set()
	def collect_websocket(func):
		from functools import partial, wraps
		@wraps(func)
		async def wrapper(*args, **kwargs):
			global connected
			connected_websockets.add(websocket._get_current_object())
			try:
				await broadcast('New connection established')
				#await asyncio.wait([ws.send('Hello!') for ws in connected])
				return await func(*args, **kwargs)
			finally:
				connected_websockets.remove(websocket._get_current_object())	
		return wrapper

	async def broadcast(msg):
		for ws in connected_websockets:
			await ws.send(msg)
	@blueprint.route('/', strict_slashes=False)
	async def http():
		"""https://github.com/pgjones/quart/blob/master/docs/websocket_tutorial.rst#5-broadcasting"""
		from quart import render_template
		return await render_template('{}/queue.html'.format(__name__.split('.')[-3]), __name__='broadcast')
	@blueprint.websocket('/', strict_slashes=False)
	@collect_websocket
	async def broadcasting():
		"""https://github.com/pgjones/quart/blob/master/docs/websocket_tutorial.rst#5-broadcasting"""
		from quart import copy_current_websocket_context
		consumer_task = asyncio.ensure_future(copy_current_websocket_context(consumer)(),)
		producer_task = asyncio.ensure_future(copy_current_websocket_context(producer)(),)
		try:
			await asyncio.gather(consumer_task, producer_task)
		finally:
			consumer_task.cancel()
			producer_task.cancel()
	
	async def consumer():
		while True:
			data = await websocket.receive()
			if data:
				await broadcast(f'echo {data}')
	async def producer():
		while True:
			await asyncio.sleep(10)
			await websocket.send('Message')
#https://gitlab.com/pgjones/quart/issues/198
#https://pgjones.gitlab.io/quart/websockets.html
#https://gitlab.com/pgjones/quart/issues/177
