

def requested_json(arg):
    from utils import get_env
    if get_env('SERVER_MODE'):
        from quart import current_app as app
    else:
        from flask import current_app as app
    if hasattr(arg, 'args'):
        return arg.headers.get('Content-Type', '').lower() == app.config.get('JSONIFY_MIMETYPE', '').lower() or 'json' in arg.args.get('json', arg.args.get('format', '')).lower()
    return arg.headers.get('Content-Type', '').lower() == app.config.get('JSONIFY_MIMETYPE', '').lower()
def get(key, default=None, args=None, *, def_key=None, _attr='args'):
    if not args:
        from utils import get_env
        if get_env('SERVER_MODE'):
            from quart import request
        else:
            from flask import request
        args = request.args
    if isinstance(args, dict):
        _x = args.get(key, def_key or None)
        if _x:
            return _x
    if hasattr(args, _attr):
        return get(getattr(args, _attr), key=key, default=default, def_key=def_key, _attr=_attr)
    return default
def get_player_id(player_name, _api, _db_model, platform='pc'):
    if not player_name:
        return -1
    player_name = player_name.lower()
    _player = _db_model.query.filter_by(name=player_name, platform=str(platform)).first()
    if not _player:
        temp = _api.getPlayerId(player_name, platform) if str(platform).isnumeric() else _api.getPlayerId(player_name)
        if not temp:
            return -1
        _player = _db_model(name=player_name, id=temp[0].playerId, platform=str(platform))
    return _player.id if _player else -1
def get_lang_id(lang=None):
    if not lang:
        lang = get_accepted_languages()
    if isinstance(lang, int):
        return lang
    return {
        'de': 2, #https://www.paladins.com/news/?lng=de_DE
        'fr': 3, #https://www.paladins.com/news/?lng=fr_FR
        'es': 9, #https://www.paladins.com/news/?lng=es_LA
        'pt': 10, #https://www.paladins.com/news/?lng=pt_BR
        'ru': 11, #https://www.paladins.com/news/?lng=ru_RU
        'pl': 12, #https://www.paladins.com/news/?lng=pl_PL | Polski
        'tr': 13 #https://www.paladins.com/news/?lng=tr_TR
    }.get(lang, 1) #https://www.paladins.com/news/?lng=en_US#5, 7,
def get_accepted_languages():
    from utils import get_env
    if get_env('SERVER_MODE', None):
        from quart import request
    else:
        from flask import request
    from utils import LanguagesSupported
    return str(request.accept_languages).split('-')[0] if request.accept_languages else LanguagesSupported.English.value

def get_config(x=None, y='config.'):
    return y + {
        'development': 'Developement',
        'dev': 'Developement',
        'testing': 'Testing',
        'default': 'Production',
        'production': 'Production',
        'prod': 'Production'
    }.get(str(x).lower(), 'Production')

def get_language():
    from utils import LanguagesSupported
    aux = str(get('language', default=get_accepted_languages())).lower()
    try:
        return LanguagesSupported(aux).value
    except ValueError:
        return LanguagesSupported.English.value

def load_locate_json(message, lang=None, *, force=False, folder='lang'):
    from utils import get_env
    if get_env('SERVER_MODE', None):
        from quart import g
    else:
        from flask import g
    if force or '_json' not in g:
        from utils import load_locate_json as _load
        g._json = _load(lang=lang or get_language(), folder=folder)
    return g._json.get(str(message).upper(), message)# or message

def is_async():
    from utils import get_env
    return get_env('SERVER_MODE', None)

def supports_quart(force_async=False):
  import sys
  return sys.version_info >= (3, 7, 0) and (force_async or is_async())
def create_blueprint(name, import_name, *, package=None, force_async=False, **options):
  try:
    import importlib
    module = importlib.import_module(package)# or 'flask'
  except (ImportError, AttributeError):
    if supports_quart(force_async):
        package, force_async = 'quart', True
    return create_blueprint(name=name, import_name=import_name, package=package or 'flask', force_async=force_async, **options)
  return module.Blueprint(name, import_name, **options)
'''
  if sys.version_info > (3, 7, 0) and (force_async or get_env('ASYNC', None)):
    from quart import Blueprint
    return Blueprint(name, import_name, **options)
  from flask import Blueprint
  return Blueprint(name, import_name, **options)
'''

def jsonify(app, response):
    if requested_json(response):#response.headers.get('Content-Type', '').lower() == app.config['JSONIFY_MIMETYPE'].lower():
        from flask import request
        _indent_, separators = None, (',', ':')
        if request.args.get('format', 'json') in ['json_pretty', 'pretty'] or app.config['JSONIFY_PRETTYPRINT_REGULAR']:
            _indent_, separators = 2, (',', ': ')
        import json
        from datetime import datetime, timedelta, timezone
        from email.utils import format_datetime
        response.set_data(json.dumps(response.get_json(), sort_keys=app.config['JSON_SORT_KEYS'], ensure_ascii=app.config['JSON_AS_ASCII'], indent=_indent_, separators=(',', ':')))
        response.headers['Cache-Control'] = 'public, max-age=300'
        response.headers['Expires'] = format_datetime((datetime.utcnow() + timedelta(seconds=300)).replace(tzinfo=timezone.utc), usegmt=True)
    return response
async def ajsonify(app, response):
    if requested_json(response):#response.headers.get('Content-Type', '').lower() == app.config['JSONIFY_MIMETYPE'].lower():
        from quart import request
        _indent_, separators = None, (',', ':')
        if request.args.get('format', 'json') in ['json_pretty', 'pretty'] or app.config['JSONIFY_PRETTYPRINT_REGULAR']:
            _indent_, separators = 2, (',', ': ')
        import json
        from datetime import datetime, timedelta, timezone
        from email.utils import format_datetime
        response.set_data(json.dumps(await response.get_json(), sort_keys=app.config['JSON_SORT_KEYS'], ensure_ascii=app.config['JSON_AS_ASCII'], indent=_indent_, separators=(',', ':')))
        response.headers['Cache-Control'] = 'public, max-age=300'
        response.headers['Expires'] = format_datetime((datetime.utcnow() + timedelta(seconds=300)).replace(tzinfo=timezone.utc), usegmt=True)
    return response

def render_template(*args):
  if is_async():
    import quart
    import asyncio
    return asyncio.sync_wait(quart.templating.render_template(*args))
  from flask import render_template
  return render_template(*args)