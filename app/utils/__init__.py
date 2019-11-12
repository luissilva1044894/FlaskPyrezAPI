#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from flask import escape
class BaseEnumeration(Enum):
    def __str__(self):
        return str(self.value).lower()
    def __hash__(self):
        return hash(str(self.value).lower())
class LanguagesSupported(BaseEnumeration):
    English = 'en'
    Portuguese = 'pt'
    Spanish = 'es'
    Polish = 'pl'
class PlatformsSupported(BaseEnumeration):
    PC = 'pc'
    PTS = 'pts'
    Xbox = '10'
    PS4 = '9'
    Switch = '22'
def print_exception(exc):
    print(' : '.join([str(_) for _ in [type(exc), exc.args, exc]]))

def get_last_seen(last_seen, language=LanguagesSupported.English):
    from datetime import datetime
    delta = datetime.utcnow() - last_seen
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)
    fmt = '{y}y, {d}d' if years else '{d}d, {h}h' if days else '{h}h, {m}m' if hours else '{m}m, {s}s'
    return fmt.format(y=years, d=days, h=hours, m=minutes, s=seconds)

def replace(_input, _old, _new='', _split='', replace_or_split=False, _index=1):
    if replace_or_split:
        return _input.split(_split)[_index] or _input.replace(_old, _new)
    return _input.replace(_old, _new)

def try_int(value, default):
    try:
        return int(value)
    except ValueError:
        return default

def random(min=0, max=100, as_int=True, *, as_string=False, chars=None, size=32):
    import random
    if as_string:
        import string
        #string.punctuation
        return ''.join(random.choice(chars or (string.ascii_letters + string.digits)) for x in range(size))
    if as_int:
        return random.randint(min, max)
    return random.randrange(min, max)

def get_url(url, as_json=True):
    import requests
    _request = requests.get(url)
    if as_json:
        from json.decoder import JSONDecodeError
        try:
            return _request.json()
        except (JSONDecodeError, ValueError):
            pass
    return _request.text
def get_query(request_args, key, default_value=None, default_key=None):
    _x = request_args.get(key, default_key or None)
    if not _x:
        return default_value
    return _x
def getPlayerName(request_args):
    qry = request_args.get('query', default=None)
    if qry:
        playerName = qry[1:qry.rfind('"')] if qry.rfind('"') > 1 else qry.split(' ')[0]
    else:
        playerName = request_args.get('player', default=None)#str(request_args.get('query', default=str(request_args.get('player', default=None)).lower()).split(' ')[0]).lower()
    return None if not playerName or len(playerName) < 4 or (playerName.lower() in ['none', '0', 'null', '$(1)', 'query=$(querystring)', '[invalid%20variable]', 'your_ign', '$target']) else escape(playerName)

def getPlatform(request_args):
    qry = request_args.get('query', default=None)
    if qry:
        aux = qry[qry.rfind('"')+1:].split(' ') if qry.rfind('"') > 1 else qry.split(' ')
        if isinstance(aux, (type(()), type([]))) and len(aux) > 1:
            aux = aux[len(aux) - 1]
        else:
            aux = str(request_args.get('platform', default=None)).lower()
    else:
        aux = str(request_args.get('platform', default=None)).lower()
    return PlatformsSupported.Xbox if aux.startswith('xb') else PlatformsSupported.Switch if aux.startswith('switch') else PlatformsSupported.PS4 if aux.startswith('ps') else PlatformsSupported.PTS if aux.startswith('pts') else PlatformsSupported.PC
def winratio(wins, matches_played):
        _w = wins /((matches_played) if matches_played > 1 else 1) * 100.0
        return int(_w) if _w % 2 == 0 else round(_w, 2)


#def get_json(filename='langs'):
#    from flask import g
#    if '_json' not in g:
#        from app.utils.file import read_json
#        g._json = read_json(filename + '.json')
#    return g._json
def get_json(lang='en', *, key=None, force=False, folder='lang/'):
    from flask import g
    if force or '_json' not in g:
        from app.utils.file import read_json
        g._json = read_json('{}{}.json'.format(folder, lang))
    if key:
        return g._json[key]
    return g._json
def fix_url_for(_json, blueprint_name):
    from flask import url_for
    for _ in range(len(_json['HTML']['CMD_TABLE'][blueprint_name.upper()])):
        for __ in range(len(_json['HTML']['CMD_TABLE'][blueprint_name.upper()][_])):
            #input(_json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__])
            if _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__]:
                if _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__].startswith('url_for'):
                    _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__] = url_for('{}.{}'.format(blueprint_name, _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__].split(':')[1]), _external=True)
    return _json

def get_env(name, default=None, verbose=False):
    import os
    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
        #try:
        #    return os.environ[name] or default
        #except KeyError:
        #    return default
    else:
        #from pathlib import Path  # python3 only
        load_dotenv(verbose=verbose)#,dotenv_path=Path('.') / '.env'
    finally:
        return os.getenv(name) or default

def to_bool(value=None):
    """
    https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python

    >>> import json
    >>> json.loads("false".lower())
    False
    >>> json.loads("True".lower())
    True
    """
    if isinstance(value, bool):
        return value
    return { #if lower_value in valid: return valid[lower_value]
        '1': True, 'true': True, 't': True, 'on': True, 'yes': True,
        '0': False, 'false': False, 'f': False, 'off': False, 'no': False,
    }.get(str(value).lower(), False)#if not isinstance(value, basestring):
