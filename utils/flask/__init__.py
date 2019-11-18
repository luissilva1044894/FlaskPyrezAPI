
def get(key, default=None, args=None, *, def_key=None, _attr='args'):
    if not args:
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
    from flask import g
    if force or '_json' not in g:
        from utils import load_locate_json as _load
        g._json = _load(lang=lang or get_language(), folder=folder)
    return g._json.get(str(message).upper(), message)# or message
def create_blueprint(name, *, static_url_path='', url_prefix='', split_index=1):
    from flask import Blueprint
    return Blueprint(name.split('.', 1)[split_index], name, static_url_path=static_url_path, url_prefix=static_url_path)



