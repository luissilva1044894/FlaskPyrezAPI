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
