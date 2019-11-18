#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .player import Paladins, Smite
from .session import Session
from .paladins.server import Platform, Server, PatchNote
