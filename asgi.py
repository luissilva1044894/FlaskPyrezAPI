
def get_path(path, folder, _dir='data'):
	import os
	return os.path.join(path, _dir, folder)

def load_config(app, _env_name='FLASK_ENV', _config_filename='config.cfg'):
	from utils import get_env
	from utils.flask import get_config
	import os

	app.config.from_object(get_config(get_env(_env_name, default='dev' if os.sys.platform == 'win32' or os.name == 'nt' else 'prod')))
	app.config.from_pyfile(_config_filename, silent=True)

def create_app(app_name=None, *, static_folder=None, template_folder=None, static_url_path=None, instance_relative_config=True):
	from quart import Quart
	app_name = app_name or __name__.split('.')[0]
	root_path = __file__[:__file__.rfind(app_name)]
	print(app_name, root_path)
	app = Quart('web', static_folder=static_folder or get_path(root_path, 'static'), template_folder=template_folder or get_path(root_path, 'templates'), static_url_path=static_url_path or '', instance_relative_config=instance_relative_config)

	load_config(app)

	return app

app = create_app()

@app.before_serving
async def startup():
	print('before_serving')

@app.after_serving
async def cleanup():
    print('after_serving')
@app.route('/')
async def hello():
    return 'Hello World!'

from utils import create_blueprint
blueprint = create_blueprint('api', __name__, static_url_path='', url_prefix='/api', force_async=True, package='quart')

@blueprint.route('/a/')
async def a_():
	return '???'
if __name__ == '__main__':
	import asyncio
	from utils.loop import get_event_loop
	asyncio.set_event_loop(get_event_loop())

	app.register_blueprint(blueprint)
	#from web.api.twitch import views
	#app.register_blueprint(views.blueprint)
	app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
