#!/usr/bin/python

from flask import Blueprint, render_template, request

paladins = Blueprint("paladins", __name__, static_folder="static", template_folder="templates", static_url_path='')

@paladins.route('/', methods=["GET"])
#@paladins.route('/<>')
def index():
	from .. import index

	#print(request.blueprint)

	return index()
