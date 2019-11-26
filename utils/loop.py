
def get_event_loop(debug=False):
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
			asyncio.set_event_loop(uvloop.new_event_loop())
	if sys.platform == 'win32':
		asyncio.set_event_loop(asyncio.ProactorEventLoop())
	else:
		asyncio.set_event_loop(asyncio.new_event_loop())#asyncio.get_event_loop_policy().new_event_loop()
	#loop.set_debug(False)
	return asyncio.get_event_loop()
