
import aiohttp
import asyncio

import logging
log = logging.getLogger(__name__)

class Client:
	"""Client for interacting with HTTP"""

	def __init__(self, *, user_agent=None, session=None, loop=asyncio.get_event_loop()):
		self.session = session or aiohttp.ClientSession(loop=loop)
		self.headers = {'User-Agent': user_agent or 'XXX {} (github.com/YYY/WWW) discord.py/aiohttp'.format('0.0.1')}
	async def request(self, method, url, json=False, **kwargs):
		"""Makes a HTTP request: DO NOT call this function yourself - use provided methods"""
		async with self.session.request(method, url, **kwargs) as r:
			log.debug(f'{r.method} [{r.url}] {r.status}/{r.reason}')
			if r.headers['Content-Type'] == 'application/json' or json:
				return await r.json()
			else:
				return await r.text()
	async def get(self, url, *, headers={}, json=False, **kwargs):
		"""Make a GET request

		Params
		------
		url : str
			The URL to make the request to
		headers : dict
			Additional headers to send with the request
		json : bool
			Force returning as JSON
		Returns
		-------
		dict [or str]
			If result was not JSON, returns str
		"""
		return await self.request('GET', url, headers={**self.headers, **headers}, **kwargs)
