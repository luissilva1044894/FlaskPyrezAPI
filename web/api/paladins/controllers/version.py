
def create_platform_dict(arg):
  #_data = {}
  #_data [arg.platform if arg.platform.lower() != 'pts' else 'pts'] = {'limited_access': arg.limitedAccess, 'status': arg.status, 'version': arg.version}
  #return _data
  #print(arg.platform if arg.platform.lower() != 'pts' else 'pts', arg.platform)
  return {'name': arg.platform if arg.environment.lower() != 'pts' else arg.environment, 'limited_access': arg.limitedAccess, 'status': arg.status, 'version': arg.version}

def jsonify_func(args):
  print(args['ping'])
  #for _ in args['status']:
  #  input(create_platform_dict(_))
  return {
    "game": "paladins",
    "version": "2.11",
    "api_version": "0.0.41",
    #"platform": [{_: create_platform_dict(_)} for _ in args['status']], recursão infinita
    "platform": [create_platform_dict(_) for _ in args['status']],
    #"platform": {create_platform_dict(_) for _ in args['status']},
    "patch_notes": {},
    "ret_msg": None
  }
def func(_api, as_json=False):
  from utils import get_url
  _title = get_url('https://cms.paladins.com/wp-json/api/get-posts/1?&search=update%20notes')[0].get('title')
  _patch_notes = get_url('https://cms.paladins.com/wp-json/api/get-posts/1?&search={}'.format(_title[:_title.rfind('update') - 1]))
  print(_patch_notes)
  _server_status, _ping = _api.getServerStatus(), _api.ping()
  if as_json:
    from flask import jsonify
    return jsonify(jsonify_func({'status': _server_status, 'ping': _ping}))
  return 'api.paladins.views /api/paladins/version/;;'
"""
@app.route('/api/version', methods=['GET'])
def getGameVersion():
    try:
        language, platform = getLanguage(request), getPlatform(request.args)

        hiRezServerStatus = paladinsAPI.getServerStatus()
        hiRezServerStatus = hiRezServerStatus[1] if platform == PlatformsSupported.Xbox or platform == PlatformsSupported.Switch else hiRezServerStatus[len(hiRezServerStatus) - 2] if platform == PlatformsSupported.PS4 else hiRezServerStatus[len(hiRezServerStatus) - 1] if platform == PlatformsSupported.PTS else hiRezServerStatus[0]
        patchInfo = paladinsAPI.getPatchInfo()
    except Exception as exc:
        printException(exc)
        return UNABLE_TO_CONNECT_STRINGS[language]
    return GAME_VERSION_STRINGS[language].format('Paladins', 'Xbox One' if platform == PlatformsSupported.Xbox else 'PS4' if platform == PlatformsSupported.PS4 else 'Nintendo Switch' if platform == PlatformsSupported.Switch else 'PTS' if platform == PlatformsSupported.PTS else 'PC',
                        PALADINS_UP_STRINGS[language].format(PALADINS_LIMITED_ACCESS_STRINGS[language] if hiRezServerStatus.limitedAccess else '') if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                        patchInfo.gameVersion, hiRezServerStatus.version)
"""
