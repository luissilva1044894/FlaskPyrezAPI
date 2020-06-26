#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyrez import SmiteAPI
from utils.environ import get_env

smite_api = SmiteAPI(get_env('PYREZ_DEV_ID'), get_env('PYREZ_AUTH_ID'))
