#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os

from flask import Flask, jsonify, render_template
from flask.blueprints import Blueprint

from .config import get_config
from .models import db
from .utils.decorators import auto_register_blueprints
from utils.environ import get_env
from utils.num import try_int

def load_config(app, *, config_filename='web/config.cfg', config_name=None, env_name='FLASK_ENV', silent=True):
  # Config from object
  def get_config_name(cfg):
    if not cfg or not isinstance(cfg, str):
      if os.sys.platform == 'win32' or os.name == 'nt':
        return 'dev'
      return 'prod'
    return cfg
  app.config.from_object(get_config(get_config_name(config_name)))
  app.config.from_pyfile(config_filename, silent=silent)
  app.config.from_envvar(env_name, silent=silent) # Config from filepath in env
  #app.config.from_envvar('APP_CONFIG', silent=silent)

import logging
def setup_logger(app):
  """config logger depending on APP_ENV"""
  log_level = logging.DEBUG if app.config.get('TESTING') else logging.INFO
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
  if hasattr(app, 'init_app'):
    db.init_app(app)

  # jinja extensions
  # app.jinja_env.add_extension('jinja2.ext.do')

  return app

app = create_app()
if __name__ == '__main__':
  app.run(host=get_env('HOST', '0.0.0.0'), port=try_int(get_env('PORT'), 5000))
  #if os.environ.get('APP_LOCATION') == 'heroku':
  #  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), server='gunicorn', workers=2)
  #else:
  #  app.run(host='localhost', port=8080, debug=True)
