
from utils.web import create_blueprint

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', url_prefix='')

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
	from datetime import datetime
	def translate(message, lang=None, *, force=False, folder='lang'):
		from utils.web import load_locate_json
		return load_locate_json(message=message, lang=lang, force=force, folder=folder)
	return { 'translate': translate,  'current_year': datetime.utcnow().year}#return dict(translate=translate)

@blueprint.route('/html', methods=['GET'], strict_slashes=False)
def html_handler():
	from flask import render_template
	return render_template('base.html')
	
