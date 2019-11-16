
from flask import Blueprint
from utils import replace

blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='')#'/'

@blueprint.route('/', methods=['GET'])
@blueprint.route('/index/', methods=['GET'])
def root(error=None):
	"""Homepage route."""
	#from flask import redirect, url_for
	#return redirect(url_for('api.root'))
	return '{} IndeX'.format(blueprint.name)
#@blueprint.before_request
#@blueprint.route('/logs/<path:path>')
#def send_js(path):
#	from flask import request
#	if request.url_rule.rule:
#		print(request.url_rule.rule)
#	return send_from_directory('js', path)
@blueprint.context_processor
def utility_processor():
	def translate(message, lang=None, *, force=False, folder='lang'):
		from flask import g
		if force or '_json' not in g:
			from flask import request
			from utils import get_language
			from utils.file import read_file, join_path
			import os
			g._json = read_file(join_path(['data', folder, '{}.json'.format(lang or get_language(request))]), is_json=True)
		return g._json.get(str(message).upper(), message)# or message
	return { 'translate': translate }#return dict(translate=translate)

@blueprint.route('/html/', methods=['GET'])
def html_handler():
	from flask import render_template
	return render_template('base.html')
	
