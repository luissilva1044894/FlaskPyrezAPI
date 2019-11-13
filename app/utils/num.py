
def try_int(value, default):
    try:
        return int(value)
    except ValueError:
        return default

def random(min, max, as_int=True):
    import random
    if as_int:
        return random.randint(min, max)
    return random.randrange(min, max)

def winratio(wins, matches_played):
	_w = wins /((matches_played) if matches_played > 1 else 1) * 100.0
	return int(_w) if _w % 2 == 0 else round(_w, 2)
