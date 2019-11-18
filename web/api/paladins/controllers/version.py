
def create_platform_dict(arg):
  #_data = {}
  #_data [arg.platform if arg.platform.lower() != 'pts' else 'pts'] = {'limited_access': arg.limitedAccess, 'status': arg.status, 'version': arg.version}
  #return _data
  #print(arg.platform if arg.platform.lower() != 'pts' else 'pts', arg.platform)
  return {'name': arg.platform if arg.environment.lower() != 'pts' else arg.environment, 'limited_access': arg.limitedAccess, 'online': arg.status, 'version': arg.version}

def format_patch_notes(args):
  if args:
    _timestamp = args.get('timestamp')
    try:
      import arrow
      try:
        _timestamp = arrow.get(_timestamp, 'MMMM D, YYYY')
      except (arrow.parser.ParserMatchError, arrow.parser.ParserError):
        pass
      else:
        _timestamp = _timestamp.isoformat()#_timestamp.format('DD-MMM-YYYY HH:mm:SS ZZ')
        # 2019-11-12T23:31Z | 2019-11-18T18:36:32+00:00
    except importError:
      pass
    return {'author': args.get('author'), 'content': args.get('content'), 'image': { 'thumb': args.get('image'), 'header': args.get('featured_image') }, 'timestamp': _timestamp, 'title': args.get('title')}
  return None

def jsonify_func(args):
  print(args['ping'])
  return {
    'game': args['ping'].apiName[:-3].lower(),
    'version': args['ping'].gamePatch,
    'api_version':args['ping'].apiVersion,
    #"platform": [{_: create_platform_dict(_)} for _ in args['status']], recursão infinita
    'platform': [create_platform_dict(_) for _ in args['status']],
    'latest_patch_notes': [format_patch_notes(_) for _ in args['patch_notes']],
  }
def func(_api, as_json=False, lang='1'):
  _server_status, _ping = _api.getServerStatus(), _api.ping()
  if as_json:
    from utils import get_url
    _title = get_url('https://cms.paladins.com/wp-json/api/get-posts/1?&search=update%20notes')[0].get('title')
    _patch_notes, _patch_note = get_url('https://cms.paladins.com/wp-json/api/get-posts/1?&search={}'.format(_title[:_title.rfind('update') - 1])), []
    for i in range(len(_patch_notes)):
      x = get_url('https://cms.paladins.com/wp-json/api/get-post/{}?&slug={}'.format(lang, _patch_notes[i].get('slug')))
      x.update({'image': _patch_notes[i].get('featured_image')})
      _patch_note.append(x)
    print(_patch_notes)

    from flask import jsonify
    return jsonify(jsonify_func({'status': _server_status, 'ping': _ping, 'patch_notes': _patch_note}))
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
