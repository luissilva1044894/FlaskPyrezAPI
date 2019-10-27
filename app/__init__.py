# -*- coding: utf-8 -*-

#https://danidee10.github.io/2016/11/20/flask-by-example-8.html
#https://exploreflask.com/en/latest/blueprints.html
#https://flask.palletsprojects.com/en/1.1.x/patterns/urlprocessors/#internationalized-blueprint-urls
#https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/

def register(app):
	from .views import blueprint
	from .utils import replace
	app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app', 'api')))

	from .overwatch import register as overwatch_reg
	from .paladins import register as paladins_reg
	from .twitch import register as twitch_reg
	overwatch_reg(app)
	paladins_reg(app)
	twitch_reg(app)
