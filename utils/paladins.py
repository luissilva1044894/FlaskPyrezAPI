
def get_dmg_type(arg, as_int=False):
	if as_int:
		return { 'true': 0, 'aoe': 1, 'physical': 2, 'direct': 3 }.get(arg.lower(), -1)
	return { 0: 'True', 1: 'AoE', 2: 'Physical', 3: 'Direct' }.get(arg, 'Unknown')

def get_item_type(arg, as_int=False):
	if as_int:
		return { 'utility': 0, 'healing': 1, 'defense': 2, 'damage': 3 }.get(arg.lower(), -1)
	return { 0: 'Utility', 1: 'Healing', 2: 'Defense', 3: 'Damage' }.get(arg, 'Unknown')

def extract_description(description, pattern=r'\[(.+?)\] (.*)'):
	import re
	match = re.compile(pattern).match(description)
	if match:
		return match.group(2).strip(), match.group(1)
	#description = re.sub('[\[].*?[\]] ', '', description)
	return description, None

def extract_scale(description, pattern=('=(.+?)\|', '{(.*?)}')):
	import re
	_search = re.search(pattern[0], description)
	_scale = -1
	try:
		_scale = float(str(_search.group(1)).replace(',', '.'))
	except AttributeError:
		pass
	'''
	else:

		print(_scale % 2 in [0, 1], not _scale % 2 == _scale, _scale, int(_scale))
		if _scale % 2 in [0, 1]: _scale = int(_scale)#_scale % 2 == 0 and not (_scale % 2 == _scale)
	'''
	try:
		description = description.replace('{' + str(re.search(pattern[1], description).group(1)) + '}', '{SCALE}')
	except AttributeError:
		pass
	return _scale, description

'''
self.ability = None
match = re.compile(r'\[(.+?)\] (.*)').match(description)
if match:
  self.ability = match.group(1)
  description = match.group(2).strip()
self.is_talent = boolify(is_talent)
self.description = description
match = re.compile(r'\[(.+?)\] (.*)').match(short_desc)
if match:
  short_desc = match.group(2).strip()

import re
scale = re.search('=(.+?)\|', description)
try:
  self.scale = float(str(scale.group(1)).replace(',', '.'))
  # if scale % 2 == 0 or scale % 2 == scale: scale = int(scale)
except AttributeError:
  pass
try:
  description = description.replace('{' + str(re.search('{(.*?)}', description).group(1)) + '}', '{SCALE}')
except AttributeError:
  pass
'''
