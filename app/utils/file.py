
def open_if_exists(filename, mode='rb', encoding='utf-8'):
    """Returns a file descriptor for the filename if that file exists, otherwise ``None``."""
    import os

    #os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))) # allow setup.py to be run from any path
    import glob
    print(os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('app\\utils', ''), filename))
    print([f for f in glob.glob("**/", recursive=True) if f.rfind('__') == -1])

    app_dir = os.path.abspath(os.path.dirname(__file__))

    #print(os.listdir())
    print(['{}'.format(f) for f in os.listdir() if not f.startswith('__')])
    #print(os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('app\\utils', ''), filename))
    #print(app_dir.replace('app\\utils', '') + filename)
    #print('EXIST: {} '.format(os.path.isfile(filename)))
    #print('EXIST: {} '.format(os.path.isfile(''.join([app_dir.replace('app\\utils', ''), filename]))))
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
