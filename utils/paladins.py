
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
	_scale = None
	try:
		_scale = float(str(scale.group(1)).replace(',', '.'))
		# if scale % 2 == 0 or scale % 2 == scale: scale = int(scale)
	except AttributeError:
		pass
	try:
		description = description.replace('{' + str(re.search(pattern[1], description).group(1)) + '}', '{SCALE}')
	except AttributeError:
		pass
	return _scale, description
