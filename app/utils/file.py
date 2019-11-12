
def open_if_exists(filename, mode='rb', encoding='utf-8'):
    """Returns a file descriptor for the filename if that file exists, otherwise ``None``."""
    import os
    print('EXIST: {} '.format(os.path.isfile(filename)))
    if not os.path.isfile(filename):
    	return None
    return open(filename, mode=mode)#, encoding=encoding)

def read_json(filename, mode='rb', encoding='utf-8'):
	import json
	_file = open_if_exists(filename, mode, encoding)
	if _file:
		with _file as f:
			return json.load(f)
	return {}
	#from json.decoder import JSONDecodeError
	#try:
	#except json.decoder.JSONDecodeError:
	#	pass
