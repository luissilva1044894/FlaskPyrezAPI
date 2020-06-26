#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  jsonify,
  render_template,
)

from utils.web import create_blueprint

app = create_blueprint(__name__)

# Sample main page
@app.route('/')
def home():
  """Homepage route."""
  return render_template('index.html')

@app.route('/hello/<name>', methods=['GET'])
def hello_someone(name):
  return render_template('index.html', name=name.title())

@app.route('/hello')
def hello():
  return 'Hello, World!'

# Sample setup script
@app.route('/setup/', strict_slashes=False)
def setup_route():
  data = {
    'worked': True,
    'msg': 'It worked!'
  }
  return jsonify(data)
