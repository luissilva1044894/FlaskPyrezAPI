
def open_if_exists(filename, mode='rb', encoding='utf-8'):
    """Returns a file descriptor for the filename if that file exists, otherwise ``None``."""
    import os
    if not os.sys.platform == 'win32' or not os.name == 'nt':
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
    #https://www.guru99.com/reading-and-writing-files-in-python.html
    try:
        return open(filename, mode=mode, encoding=encoding)
    except ValueError:
        return open(filename, mode=mode)
def join_path(arr, relative_path=True):
    import os
    _j = ''
    if relative_path:
        _j = os.path.dirname(__file__).replace(__name__.split('.')[0], '')
    for _ in arr:
        _j = os.path.join(_j, _)
    return _j
def delete_folder(folder_path, recursive=True):
    from shutil import rmtree
    try:
        rmtree(folder_path)
    except OSError:
        pass
def create_folder(folder_path):
    import os
    if not os.path.isdir(folder_path):
        from os import mkdir
        mkdir(folder_path)
def recreate_folder(folder_path):
    delete_folder(folder_path)
    create_if_inexistent(folder_path)
def read_file(filename, *, mode='rb', encoding='utf-8', is_json=False):
    """Loads a file"""
    _file = open_if_exists(filename, mode, encoding)
    if is_json:
        if _file:
            with _file as f:
                import json
                from json.decoder import JSONDecodeError
                try:
                    return json.load(f)
                except json.decoder.JSONDecodeError:
                    pass
        return {}
    return _file
def write_file(filename, content, *, mode='w', is_json=False):
    with open(filename, mode) as f:
        if is_json:
            import json
            json.dump(content, f, ensure_ascii=True, indent=4)
        else:
            f.write(content)
