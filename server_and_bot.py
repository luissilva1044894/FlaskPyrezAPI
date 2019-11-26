
from web import create_app
app = create_app(is_async=True)

@app.before_serving
async def startup():
	print('before_serving')

@app.after_serving
async def cleanup():
	print('after_serving')
@app.route('/')
async def hello():
	return 'Hello World!'

@app.route('/render')
async def index():
	from quart import render_template
	return await render_template('index.html')

@app.route('/video')
async def auto_video():
	# Automatically respond to the request
	from quart import send_file
	return await send_file('data/video.mp4', conditional=True)

@app.route('/chunked')
async def chunked_video():
	from quart import request, send_file
	# Force the response to be chunked in a 100_000 bytes max size.
	response = await send_file('data/video.mp4')
	await response.make_conditional(request.range, max_partial_size=100_000)
	return response

@app.route('/a/')
async def a_():
	return 'Hello from {}'.format(bot.user.name)
if __name__ == '__main__':
	'''https://gist.github.com/crrapi/c8465f9ce8b579a8ca3e78845309b832'''
	import asyncio
	from utils.loop import get_event_loop
	asyncio.set_event_loop(get_event_loop())

	from threading import Thread
	from functools import partial

	partial_run = partial(app.run, debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
	Thread(target=partial_run).start()

	from discord_bot import Bot
	from utils import get_env
	bot = Bot()
	bot.config.from_object('config.Discord')
	bot.config.from_pyfile('config/discord.cfg', silent=True)
	bot.run(debug=True)
