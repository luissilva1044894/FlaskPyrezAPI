#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import create_blueprint

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', template_folder='templates', url_prefix='/{}'.format('/'.join(__blueprint__name[:-1])))

# Assuming urls.db is in your app root folder
from web.models import db
class Post(db.Model):
  __tablename__ = 'WEB_URL'
  from sqlalchemy.schema import Sequence
  id = db.Column(db.Integer(), Sequence('WEB_URL_id_seq', start=1, increment=1), primary_key=True)
  url = db.Column(db.LargeBinary(), unique=True)

  def __init__(self, url):
  	import base64
  	self.url = base64.urlsafe_b64encode(url)

def to_base_62(num, b=62):
	import string
	try:
		from string import ascii_lowercase
		from string import ascii_uppercase
	except ImportError:
		from string import lowercase as ascii_lowercase
		from string import uppercase as ascii_uppercase
	from math import floor
	if b <= 0 or b > 62:
		return 0
	base = string.digits + ascii_lowercase + ascii_uppercase
	r = num % b
	res = base[r]
	q = floor(num / b)
	while q:
		r = q % b
		q = floor(q / b)
		res = base[int(r)] + res
	return res

def to_base_10(num, b=62):
	import string
	try:
		from string import ascii_lowercase
		from string import ascii_uppercase
	except ImportError:
		from string import lowercase as ascii_lowercase
		from string import uppercase as ascii_uppercase
	base = string.digits + ascii_lowercase + ascii_uppercase
	limit = len(num)
	res = 0
	for i in range(limit):
		res = b * res + base.find(num[i])
	return res

@blueprint.route('/', methods=['GET'])
def home_get():
	from flask import render_template
	return render_template('home.html')

@blueprint.route('/', methods=['POST'])
def home_post():
	from flask import request, render_template, url_for
	try:
		from urllib.parse import urlparse  # Python 3
		str_encode = str.encode
	except ImportError:
		from urlparse import urlparse  # Python 2
		str_encode = str
	original_url = str_encode(request.form.get('url'))
	pf = Post('https://' + original_url if urlparse(original_url).scheme == '' else original_url)
	db.session.add(pf)
	db.session.commit()
	encoded_string = to_base_62(pf.id)
	return render_template('home.html', short_url=url_for('.home_get') + encoded_string)

@blueprint.route('/<short_url>', methods=['GET'])
def redirect_short_url(short_url):
	from flask import redirect, url_for
	import base64
	p = Post.query.filter_by(id=to_base_10(short_url)).first() # converting into decimal format
	if p:
		print(base64.urlsafe_b64decode(p.url))
		redirect(base64.urlsafe_b64decode(p.url))
	return redirect(url_for('.home_get'))# fallback if no URL is found
