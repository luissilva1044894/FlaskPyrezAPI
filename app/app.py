#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
from flask import Flask, jsonify, render_template
from flask.blueprints import Blueprint

from config import get_config
from utils.web.decorators import auto_register_blueprints
from .models import db

def load_config(app, _env_name='FLASK_ENV', _config_filename='config.cfg'):
  # Config from object
  app.config.from_object(get_config('dev' if os.sys.platform == 'win32' or os.name == 'nt' else 'prod'))
  app.config.from_pyfile(_config_filename, silent=True)
  app.config.from_envvar('APP_CONFIG', silent=True) # Config from filepath in env

import logging
def setup_logger(app):
  """config logger depending on APP_ENV"""
  log_level = logging.DEBUG if app.config.get("TESTING") else logging.INFO
  log_format = "[%(asctime)s] {%(filename)s#%(funcName)s:%(lineno)d} %(levelname)s - %(message)s"
  handler = logging.StreamHandler()
  handler.setLevel(log_level)
  handler.setFormatter(logging.Formatter(log_format))
  app.logger.addHandler(handler)
  app.logger.setLevel(log_level)
  # remove default Flask debug handler
  del app.logger.handlers[0]
  return app

@auto_register_blueprints#(call_method='register_blueprint', instance_of=Blueprint)
def create_app(name=None, static_folder='static', template_folder='templates', static_url_path=''):
  app = Flask(name or __name__, static_folder=static_folder, template_folder=template_folder, static_url_path=static_url_path)

  load_config(app)
  #print(app.config)
  # define logging patterns
  app = setup_logger(app)
  db.init_app(app)

  # jinja extensions
  # app.jinja_env.add_extension('jinja2.ext.do')

  return app

app = create_app()
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
