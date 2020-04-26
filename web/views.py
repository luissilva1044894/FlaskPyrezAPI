
from flask import render_template#, request, redirect, url_for

from utils.web import create_blueprint, load_locate_json

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', url_prefix='')

@blueprint.route('/', methods=['GET'])
@blueprint.route('/index/', methods=['GET'])
def root(error=None):
	"""Homepage route."""
	#return redirect(url_for('api.root'))
	return f'{blueprint.name} IndeX'
#@blueprint.before_request
#@blueprint.route('/logs/<path:path>')
#def send_js(path):
#	if request.url_rule.rule:
#		print(request.url_rule.rule)
#	return send_from_directory('js', path)

@blueprint.context_processor
def utility_processor():
  def translate(message, lang=None, *, force=False, folder='lang'):
    return load_locate_json(message=message, lang=lang, force=force, folder=folder)
  return { 'translate': translate}#return dict(translate=translate)

@blueprint.route('/html', methods=['GET'], strict_slashes=False)
def html_handler():
  return render_template('base.html')
