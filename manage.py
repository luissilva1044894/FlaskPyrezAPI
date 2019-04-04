from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_command("debug", Server(host="0.0.0.0", port=8080, use_debugger=True))

if __name__ == "__main__":
    #db.create_all()
    manager.run()
