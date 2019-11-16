#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from web import app

#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate, MigrateCommand

#from web.factory import create_app
#app = create_app()

manager = Manager(app)
manager.add_command('debug', Server(host='127.0.0.1', port=8080, use_debugger=True))
#@manager.command
#def debug():
#	app.run(host='127.0.0.1', port=8080, use_debugger=True, debug=True)

#migrate = Migrate(app, app._extensions['db'])
#manager.add_command('db', MigrateCommand)

#@manager.command
#def create_db(drop_db=False):
#	if drop_db:
#		app._extensions['db'].drop_all()
#	app._extensions['db'].create_all()

if __name__ == '__main__':
	try:
		import psutil
	except ImportError:
		pass
	else:
		import os
		for q in psutil.process_iter():
			if q.name().startswith('python'):
				if q.pid != os.getpid() and [_ for _ in q.cmdline() if os.path.basename(__file__) in _]:
					import sys
					print(f'App is already running!')#Bot is already running!
					sys.exit()
	manager.run()
