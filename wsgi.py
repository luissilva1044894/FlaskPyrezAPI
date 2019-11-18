#from web import app as application
from web import create_app

app = create_app()
app.app_context().push()

#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)
if __name__ == '__main__':
	app.run(debug=app.config['DEBUG'], use_debugger=app.config['DEBUG'], use_reloader=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
