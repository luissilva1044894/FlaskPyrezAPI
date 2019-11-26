#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import is_async
if is_async():
	from utils.web import create_blueprint
	blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format('/'.join(__name__.split('.')[1:-1])))

	@blueprint.route('/')
	async def index():
		"""https://gitlab.com/pgjones/quart/blob/master/examples/video/video.py"""
		from quart import render_template
		return await render_template('stream_video.html')

	@blueprint.route('/video')
	async def auto_video():
		# Automatically respond to the request
		from quart import send_file
		return await send_file('data/video.mp4', conditional=True)
		#return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

	@blueprint.route('/chunked')
	async def chunked_video():
		from quart import request, send_file
		# Force the response to be chunked in a 100_000 bytes max size.
		response = await send_file('data/video.mp4')
		await response.make_conditional(request.range, max_partial_size=100_000)
		return response
"""
>>> from socket import gethostname
>>> gethostname()
'Luis-PC'

#https://pgjones.gitlab.io/quart/async_compatibility.html
import asyncio
def main():
  print('sync')
  import time
  time.sleep(3)
async def a_main():
  await asyncio.coroutine(main)()
  print('async')
  asyncio.sleep(2)
def example():
  asyncio.run(a_main())

@app.route('/user/<username>')
def profile(username):
	return '{}\'s profile'.format(escape(username))

print(url_for('login', next='/'))
print(url_for('profile', username='John Doe'))

@app.route('/uploads/<path:filename>')
def download_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

ConfigAttribute
config_class = Config


self.config = self.make_config(instance_relative_config)


root_path = self.root_path
if instance_relative:
  root_path = self.instance_path      
return self.config_class(root_path, defaults)


self.import_name = import_name
if root_path is None:
   root_path = get_root_path(self.import_name)
self.root_path = root_path


rv = self.config['PRESERVE_CONTEXT_ON_EXCEPTION']
if rv:
  return rv
return self.debug

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import yourapplication.models
    Base.metadata.create_all(bind=engine)

class methods: cls as first parameter
instance methods: self as first parameter
lambdas for properties might have the first parameter replaced with x like in display_name = property(lambda x: x.real_name or x.username)

https://flask.palletsprojects.com/en/1.1.x/extensiondev/#anatomy-of-an-extension
https://flask.palletsprojects.com/en/1.1.x/styleguide/#general-layout
https://diveintohtml5.info/

import sys
path = '/home/yourusername/mysite'
if path not in sys.path:
	sys.path.insert(0, path)

from socket import gethostname
[...]
if __name__ == '__main__':
	db.create_all()
	if 'liveconsole' not in gethostname():
		app.run()

https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/
"""