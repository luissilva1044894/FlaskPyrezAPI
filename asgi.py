
def get_path(path, folder, _dir='data'):
	import os
	return os.path.join(path, _dir, folder)

'''
def create_app(app_name=None, *, static_folder=None, template_folder=None, static_url_path=None, instance_relative_config=True):
	from quart import Quart
	app_name = app_name or __name__.split('.')[0]
	root_path = __file__[:__file__.rfind(app_name)]
	print(app_name, root_path)
	app = Quart('web', static_folder=static_folder or get_path(root_path, 'static'), template_folder=template_folder or get_path(root_path, 'templates'), static_url_path=static_url_path or '', instance_relative_config=instance_relative_config)

	load_config(app)

	return app
'''
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

from utils.web import create_blueprint
blueprint = create_blueprint('api', __name__, static_url_path='', url_prefix='/api', force_async=True, package='quart')

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

@blueprint.route('/a/')
async def a_():
	return '???'
if __name__ == '__main__':
	#import asyncio
	#from utils.loop import get_event_loop
	#asyncio.set_event_loop(get_event_loop())

	app.register_blueprint(blueprint)
	#from web.api.twitch import views
	#app.register_blueprint(views.blueprint)
	app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
