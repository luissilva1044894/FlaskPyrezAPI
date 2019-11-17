#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
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

def get_accepted_languages(request_args):
    return str(request_args.accept_languages).split('-')[0] if request_args.accept_languages else LanguagesSupported.English.value
def get_language(request_args):
    aux = str(request_args.args.get('language', default=get_accepted_languages(request_args))).lower()
    try:
        return LanguagesSupported(aux).value
    except ValueError:
        return LanguagesSupported.English.value

def replace(_input, _old, _new='', _split='', replace_or_split=False, _index=1):
    if replace_or_split:
        return _input.split(_split)[_index] or _input.replace(_old, _new)
    return _input.replace(_old, _new)

def random(min=0, max=100, *, as_int=True, args=None):
    import random
    if args:
        return random.choice(args)#if isinstance(args, list) and len(args) > 0:
    if as_int:
        return random.randint(min, max)
    return random.randrange(min, max)

def random_string(chars=None, size=32):
    from random import choice
    if not chars:
        import string
        chars = string.ascii_letters + string.digits # + string.punctuation
    return ''.join(choice(chars) for _ in range(size))

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
def get(args, key, default=None, *, def_key=None, _attr='args'):
    if isinstance(args, dict):
        _x = args.get(key, def_key or None)
        if _x:
            return _x
    if hasattr(args, _attr):
        return get(getattr(args, _attr), key=key, default=default, def_key=def_key, _attr=_attr)
    return default

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

def create_blueprint(name, *, static_url_path='', url_prefix='', split_index=1):
    from flask import Blueprint
    return Blueprint(name.split('.', 1)[split_index], name, static_url_path=static_url_path, url_prefix=static_url_path)
def get_config(x=None, y='config.'):
    return y + {
        'development': 'Developement',
        'dev': 'Developement',
        'testing': 'Testing',
        'default': 'Production',
        'production': 'Production',
        'prod': 'Production'
    }.get(str(x).lower(), 'Production')

"""
https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python

>>> import json
>>> json.loads("false".lower())
False
>>> json.loads("True".lower())
True
"""
