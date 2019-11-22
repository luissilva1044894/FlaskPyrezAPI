
def open_if_exists(filename, mode='rb', encoding='utf-8'):
  """Returns a file descriptor for the filename if that file exists, otherwise ``None``."""
  import os
  '''
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
  '''
  if not os.path.isfile(filename) and (mode.rfind('r') != -1 or mode.rfind('a') != -1):
    return None
  #https://www.guru99.com/reading-and-writing-files-in-python.html
  try:
    import codecs
  except ImportError:
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except ValueError:
        f = open(filename, mode=mode)
        #_io.BufferedReader
  else:
    f = codecs.open(filename, mode)
  finally:
    return f
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
  """
  Create a directory (including parents) if it does not exist yet.
  :param path: Path to the directory to create.
  :type path: :class:`pathlib.Path`
  Uses :meth:`pathlib.Path.mkdir`; if the call fails with
  :class:`FileNotFoundError` and `path` refers to a directory, it is treated
  as success.
  """
  #def mkdir_exist_ok(path):
  #    try:
  #        path.mkdir(parents=True)
  #    except FileExistsError:
  #        if not path.is_dir(): raise
def recreate_folder(folder_path):
  delete_folder(folder_path)
  create_if_inexistent(folder_path)
def read_file(filename, *, is_async=False, mode='rb', encoding='utf-8', is_json=False):
  """Loads a file"""
  if is_async:
    try:
        async def __read_file__(filename, mode='rb', encoding='utf-8', is_json=False):
            import aiofiles
            #, encoding=encoding
            try:
                async with aiofiles.open(filename, mode=mode) as f:
                    if is_json:
                        import json
                        from json.decoder import JSONDecodeError
                        try:
                            return json.loads(await f.read())
                        except json.decoder.JSONDecodeError:
                            pass
                        return {}
                    return await f.read()
            except FileNotFoundError:
                pass
        return __read_file__(filename, mode=mode, encoding=encoding, is_json=is_json)
    except ImportError:
        pass
  try:
    f = open_if_exists(filename, mode, encoding)
    if f:
        if is_json:
            import json
            from json.decoder import JSONDecodeError
            try:
                with f:
                    return json.load(f)
            except json.decoder.JSONDecodeError:
                pass
            return {}
        if f.readable():
            return f.read()#lines
        return f
  except FileNotFoundError:
    pass

def write_file(filename, content=None, *, is_async=False, mode='w', is_json=False, encoding='utf-8', indent=2, data_path=None, ensure_ascii=True, separators=(',', ':'), sort_keys=True, filetype='json'):
  """#mode='x' | 'a+'"""
  #https://www.programiz.com/python-programming/file-operation w+b

  #with open('my_file.mp3', 'w+b') as f:
  #    file_content = f.read()
  #    f.write(b'Hello')
  if data_path:
    filename = f'{data_path}/{filename}.{filetype}'
  #if content and isinstance(content, str):
  #    mode = 'wt'
  try:
    if is_async:
        try:
            async def __write_file__(filename, content=None, *, mode='w', is_json=False, encoding='utf-8', indent=2, ensure_ascii=True, separators=(',', ':'), sort_keys=True):
                import aiofiles
                async with aiofiles.open(filename, mode) as f:
                    #, encoding=encoding
                    if is_json:
                        import json
                        #await f.write(json.dump(content or {}, separators=separators, sort_keys=sort_keys, ensure_ascii=ensure_ascii, indent=indent))
                        await f.write(json.dumps(content or {}, separators=separators, sort_keys=sort_keys, ensure_ascii=ensure_ascii, indent=indent))
                    else:
                        await f.write(content or b'')
                    #import json
                    #await f.write(json.dumps(content))
            return __write_file__(filename, content=content, mode=mode, is_json=is_json, encoding=encoding, indent=indent, ensure_ascii=ensure_ascii, separators=separators, sort_keys=sort_keys)
        except ImportError:
            pass
    with open_if_exists(filename, mode, encoding) as f:
        if is_json:
            import json
            json.dump(content or {}, f, separators=separators, sort_keys=sort_keys, ensure_ascii=ensure_ascii, indent=indent)
        else:
            f.write(content or b'')
  except (FileExistsError, OSError):
    pass
#https://medium.com/python4you/python-io-streams-in-examples-97d2c4367207
