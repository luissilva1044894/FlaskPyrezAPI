# -*- coding: utf-8 -*-

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app.utils import get_env

def create_app():
	import os

	from flask import Flask
	from flask_sqlalchemy import SQLAlchemy

	def get_config(x=None):
		return {
			'development': 'config.DevelopementConfig',
            'dev': 'config.DevelopementConfig',
            'testing': 'config.TestingConfig',
            'default': 'config.ProductionConfig',
            'production': 'config.ProductionConfig',
            'prod': 'config.ProductionConfig'
	}.get(str(x).lower(), 'config.ProductionConfig')
	app = Flask(__name__.split('.')[0], static_folder='static', template_folder='templates', static_url_path='', instance_relative_config=True)
	app.config.from_object(get_config(get_env('FLASK_ENV', default='dev' if os.sys.platform == 'win32' else 'prod')))
	app.config.from_pyfile('config.cfg', silent=True)
	print(app.secret_key)

	@app.errorhandler(404)
	@app.route('/index', methods=['GET'])
	@app.route('/index.html', methods=['GET'])
	@app.route('/', methods=['GET'])
	def _root(error=None):
		from flask import redirect, url_for
		return redirect(url_for('api.root'))
	# Blueprints
	from app import register
	register(app)

	return app, SQLAlchemy(app)

app, db = create_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('debug', Server(host='127.0.0.1', port=8080, use_debugger=True))

if __name__ == '__main__':
    db.create_all()
    manager.run()
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['DEBUG'], port=int(get_env('PORT', 5000)), host='0.0.0.0')

#https://gist.github.com/rochacbruno/b1fe0ccab1a81804def887e8ed40da57
#https://gist.github.com/rochacbruno/e44c1f0f43e89093bf7ddba77ee9feef
