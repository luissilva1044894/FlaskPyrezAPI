#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.models import db, BaseModel

class Player(BaseModel):
    """Model for player accounts."""
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=False, nullable=False, autoincrement=False)#unique=True, 
    name = db.Column(db.String(120), nullable=False)
    platform = db.Column(db.String(4), nullable=False)

    def __init__(self, id, name, platform):
        self.id = id
        self.name = name
        self.platform = platform
        self.save()

class PaladinsPlayer(Player):
    __bind_key__ = 'paladins'

    #_game = db.Column(db.String(8), primary_key=False, unique=False, nullable=True, autoincrement=False)

class SmitePlayer(Player):
    __bind_key__ = 'smite'
