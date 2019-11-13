# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app

app, db = create_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('debug', Server(host='127.0.0.1', port=8080, use_debugger=True))

if __name__ == '__main__':
    db.create_all()
    manager.run()
    app.run()
#https://gist.github.com/rochacbruno/b1fe0ccab1a81804def887e8ed40da57
#https://gist.github.com/rochacbruno/e44c1f0f43e89093bf7ddba77ee9feef
