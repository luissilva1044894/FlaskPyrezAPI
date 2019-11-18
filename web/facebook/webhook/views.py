#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from utils import replace

#blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='')#'/'
blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

def handle_message(user_id, user_message):
    # DO SOMETHING with the user_message and user_id ... ¯\_(ツ)_/¯
    return "Hello "+user_id+" ! You just sent me : " + user_message
    r = requests.get('http://tinyurl.com/api-create.php?url=http://lmgtfy.com/?q='+quote(user_message))
    if r.status_code != 200:
        return 'An error occured, sry ¯\_(ツ)_/¯'
    return r.text

def handle_action(user_id, user_message):
    response = { 'recipient': {'id': user_id}, 'message': {'text': handle_message(user_id, user_message)} }
    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + os.environ.get('FB_ACCESS_TOKEN'), json=response)

def handle_message_dev(user_id, user_message):
    response = { 'recipient': {'id': user_id}, 'message': {'text': handle_message(user_id, user_message)} }
    return Response(response=json.dumps(response), status=200, mimetype='application/json')

@blueprint.route('/', methods=['GET'])
def webhook_verify():
    from flask import jsonify, request
    from utils import get_env
    VERIFY_TOKEN = get_env('FACEBOOK_VERIFY_TOKEN', None)
    if VERIFY_TOKEN:
        if request.args.get('hub.verify_token', None) == VERIFY_TOKEN:
            return request.args.get('hub.challenge', None)#request.args.get('hub.mode', '') === 'subscribe'
        return jsonify(status='error', error='Error, wrong validation token.', msg='Invalid fb verify token! Make sure this matches your webhook settings on the facebook app.'), 403
    return jsonify(status='error', name=blueprint.name), 403

@blueprint.route('/', methods=['POST'])
def webhook_action():
    from flask import request
    from utils import get_env
    import requests, json
    from flask import Response
    ACCESS_TOKEN = get_env('FACEBOOK_ACCESS_TOKEN', None)
    data = request.get_json()#json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        handle_message(entry['messaging'][0]['sender']['id'], user_id, entry['messaging'][0]['message']['text'])
    return Response(response='EVENT RECEIVED', status=200)

@blueprint.route('/dev', methods=['POST'], strict_slashes=False)
def webhook_dev():
    # custom route for local development
    import requests, json
    from flask import Response, request
    data = request.get_json()#json.loads(request.data.decode('utf-8'))
    return handle_message_dev(data['entry'][0]['messaging'][0]['sender']['id'], user_id, data['entry'][0]['messaging'][0]['message']['text'])
