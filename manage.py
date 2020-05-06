from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from main import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('debug', Server(host='127.0.0.1', port=8080, use_debugger=True))

@manager.command
def create_db():
  db.create_all()
@manager.command
def drop_db():
  db.drop_all()
@manager.command
def reset_db():
  db.drop_all()
  db.create_all()

@app.shell_context_processor
def make_shell_context():
  return dict(app=app, db=db)

if __name__ == '__main__':
  db.create_all()
  manager.run()
