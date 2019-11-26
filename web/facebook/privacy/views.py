#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import create_blueprint

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', url_prefix='/'.join([''] + __blueprint__name[:-1]))

@blueprint.route('/', methods=['GET'])
def privacy():
	# needed route if you need to make your bot public
	return 'This facebook messenger bot\'s only purpose is to [...]. That\'s all. We don\'t use it in any other way.'
