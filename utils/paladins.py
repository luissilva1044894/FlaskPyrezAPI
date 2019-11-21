
def get_dmg_type(arg, as_int=False):
	if as_int:
		return { 'true': 0, 'aoe': 1, 'physical': 2, 'direct': 3 }.get(arg.lower(), -1)
	return { 0: 'True', 1: 'AoE', 2: 'Physical', 3: 'Direct' }.get(arg, 'Unknown')
