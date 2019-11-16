#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from utils import replace

#blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='')#'/'
blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

def handle_message(user_id, user_message):
    # DO SOMETHING with the user_message ... ¯\_(ツ)_/¯
    return "Hello "+user_id+" ! You just sent me : " + user_message

@blueprint.route('/', methods=['GET', 'POST'])
def webhook_handler():
    from flask import jsonify, request
    from utils import get_env
    if request.method == 'GET':
        VERIFY_TOKEN = get_env('FACEBOOK_VERIFY_TOKEN', None)
        if VERIFY_TOKEN:
            if request.args.get('hub.verify_token', None) == VERIFY_TOKEN:
                return request.args.get('hub.challenge', None)#request.args.get('hub.mode', '') === 'subscribe'
            return jsonify(status='error', error='Error, wrong validation token.', msg='Invalid fb verify token! Make sure this matches your webhook settings on the facebook app.'), 403
        return jsonify(status='error', name=blueprint.name), 403
    import requests, json
    from flask import Response
    ACCESS_TOKEN = get_env('FACEBOOK_ACCESS_TOKEN', None)
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        user_id = entry['messaging'][0]['sender']['id']
        response = { 'recipient': {'id': user_id}, 'message': {} }
        response['message']['text'] = handle_message(user_id, entry['messaging'][0]['message']['text'])
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + ACCESS_TOKEN, json=response)
    return Response(response='EVENT RECEIVED', status=200)

@blueprint.route('/dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    import requests, json
    from flask import Response
    data = json.loads(request.data.decode('utf-8'))
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    response = { 'recipient': {'id': user_id}, 'message': {'text': handle_message(user_id, data['entry'][0]['messaging'][0]['message']['text'])} }
    return Response(response=json.dumps(response), status=200, mimetype='application/json')
