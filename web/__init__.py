#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .factory import create_app #from web.factory
#from .extensions import create_extesions
#_extesions = create_extesions()
#app = create_app(_ext=_extesions)
app = create_app()

def main():
	app.run(debug=app.config['DEBUG'], use_debugger=app.config['DEBUG'], use_reloader=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
if __name__ == '__main__':
	main()
#The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
