
def get(force_fresh=False, debug=False):
	import asyncio
	import sys
	if not debug:
		try:
			import uvloop
		except ImportError:
			print('>>> Using asyncio')
			asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
		else:
			#uvloop.install()
			print('>>> Using uvloop')
			asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
			#asyncio.set_event_loop(uvloop.new_event_loop())
	#loop.set_debug(False)
	if sys.platform == 'win32':
		if not force_fresh and isinstance(asyncio.get_event_loop(), asyncio.ProactorEventLoop) and not asyncio.get_event_loop().is_closed():
			return asyncio.get_event_loop()
		return asyncio.ProactorEventLoop()
	if force_fresh or asyncio.get_event_loop().is_closed():
		return asyncio.new_event_loop()#asyncio.get_event_loop_policy().new_event_loop() | asyncio.set_event_loop(asyncio.new_event_loop())
	return asyncio.get_event_loop()
