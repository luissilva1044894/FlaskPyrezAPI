class Config(dict):
  """
  https://github.com/pallets/flask/blob/master/src/flask/config.py
  https://pgjones.gitlab.io/quart/source/quart.utils.html#quart.utils.file_path_to_path
  https://github.com/flaskbb/flaskbb/blob/master/flaskbb/configs/default.py
  """
  def __init__(self, root_path, defaults=None):
    dict.__init__(self, defaults or {})
    self.root_path = root_path

  #def __getattribute__(self, name): return super().__getattribute__(name)
  #def __getitem__(self, key): return self.get(key.upper())

  def from_envvar(self, variable_name, silent=False):
    from utils import get_env
    rv = get_env(variable_name)
    if not rv and not silent:
      raise RuntimeError(f'Environment variable "{variable_name}" is not set'
        'and as such configuration could not be loaded.'
        'Set this variable and make it point to a configuration file')
    return self.from_pyfile(rv, silent=silent)

  def from_pyfile(self, filename, silent=False):
    import types
    import os
    filename = os.path.join(self.root_path, filename)
    d = types.ModuleType('config')
    d.__file__ = filename
    try:
      with open(filename, mode='rb') as f:
        exec(compile(f.read(), filename, 'exec'), d.__dict__)
    except IOError as e:
      if not silent and not e.errno in (errno.ENOENT, errno.EISDIR, errno.ENOTDIR):
        e.strerror = f'Unable to load configuration file ({e.strerror})'
        raise
    self.from_object(d)
    '''
    file_path = self.root_path / filename
    try:
      spec = importlib.util.spec_from_file_location("module.name", file_path)
      if spec is None:  # Likely passed a cfg file
        parser = ConfigParser()
        parser.optionxform = str  # type: ignore # Prevents lowercasing of keys
        with open(file_path) as file_:
            config_str = '[section]\n' + file_.read()
        parser.read_string(config_str)
        self.from_mapping(parser['section'])
      else:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore
        self.from_object(module)
    except (FileNotFoundError, IsADirectoryError):
      if not silent:
        raise
    '''

  def from_object(self, obj):
    if isinstance(obj, str):
      try:
        import werkzeug
        obj = werkzeug.utils.import_string(obj)
      except ImportError:
        import importlib
        try:
          path, config = obj.rsplit('.', 1)
        except ValueError:
          obj = importlib.import_module(obj)
        else:
          obj = getattr(importlib.import_module(path), config)
    for k in dir(obj):
      if k.isupper():
        self[k] = getattr(obj, k)
        #setattr(self, k.lower(), self[k])

  def from_json(self, filename, silent=False):
    import json
    import os
    filename = os.path.join(self.root_path, filename) #self.root_path / filename
    try:
      with open(filename) as f:
        return self.from_mapping(json.loads(f.read()))
    except (FileNotFoundError, IsADirectoryError, IOError) as e:
      if not silent and not e.errno in (errno.ENOENT, errno.EISDIR):
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
  '''
  def get(self, name, fallback=None):
    try:
      return self[name]
    except KeyError:
      return fallback
  '''
  def from_mapping(self, *mapping, **kwargs):
    mappings = []
    if len(mapping) == 1:
      if hasattr(mapping[0], 'items'):
        mappings.append(mapping[0].items())
      else:
        mappings.append(mapping[0])
    elif len(mapping) > 1:
      raise TypeError('expected at most 1 positional argument, got %d' % len(mapping))
    mappings.append(kwargs.items())
    for mapping in mappings:
      for (k, v) in mapping:
        if k.isupper():
          self[k] = v
          #setattr(self, k.lower(), self[k])
    '''
    mappings {}
    if mapping:
      mappings.update(mapping)
    mappings.update(kwargs)
    for key, value in mappings.items():
      if key.isupper():
        self[key] = value
    '''

  def get_namespace(self, namespace, *, lowercase=True, trim_namespace=True):
    rv = {}
    for k, v in iteritems(self):
      if k.startswith(namespace):
        if trim_namespace: key = k[len(namespace):]
        else: key = k
        if lowercase: key = key.lower()
        rv[key] = v
    return rv

  def __repr__(self):
    return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
'''
>>> class Config(object):
  A = 'A'
  B = 'B'
  C = 'C'
>>> for _ in dir(Config):
  print(_.isupper())

True
True
True
'''
