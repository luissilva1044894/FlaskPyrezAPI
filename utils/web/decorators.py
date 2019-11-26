
from functools import wraps

def cached(timeout=5 * 60, key='view/%s'):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      from flask import request
      cache_key = key % request.path
      rv = cache.get(cache_key)
      if rv:
        return rv
      rv = f(*args, **kwargs)
      cache.set(cache_key, rv, timeout=timeout)
      return rv
    return decorated_function
  return decorator

def templated(template=None):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      from . import is_async
      if is_async():
        from quart import request, render_template
      else:
        from flask import request, render_template
      template_name = template
      if template_name is None:
        template_name = request.endpoint.replace('.', '/') + '.html'
      ctx = f(*args, **kwargs)
      if not isinstance(ctx, dict):
        return ctx
      return render_template(template_name, **ctx or {})
    return decorated_function
  return decorator
def player_required(f):
  from functools import wraps
  @wraps(f)
  def decorated_function(*args, **kwargs):
    from flask import request, g
    from .__init__ import get #from . import get
    __player__ = request.headers.get('player', None) or get('player', None, args=request.args)
    if not __player__ or len(__player__) < 4:
        from .exceptions import PlayerRequired
        raise PlayerRequired
    g.__player__ = __player__
    return f(*args, **kwargs)
  return decorated_function

def champ_required(f):
  from functools import wraps
  @wraps(f)
  def decorated_function(*args, **kwargs):
    from flask import request, g
    from . import get
    __champ__ = request.headers.get('champ', None) or get('champ', None, args=request.args)
    if not __champ__ or len(__champ__) < 2:
        from .exceptions import ChampRequired
        raise ChampRequired
    g.__champ__ = __champ__
    return f(*args, **kwargs)
  return decorated_function

def restricted(access_level):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(access_level)
        return func(*args, **kwargs)
    return wrapper
  return decorator
#@restricted(access_level='admin')
def decorator(take_a_function):
  def wrapper1(take_a_function):
    def wrapper2(*takes_multiple_arguments):
        # do stuff
        return take_a_function(*takes_multiple_arguments)
    return wrapper2
  return wrapper1
def decorator2(take_a_function):
  @wraps(takes_a_function)
  def wrapper(*args, **kwargs):
    # logic here
    return takes_a_function(*args, **kwargs)
  return wrapper

#C:\Program Files\Python37\Lib\site-packages\flask\app.py#1286
# https://realpython.com/primer-on-python-decorators/
# https://pythonacademy.com.br/blog/domine-decorators-em-python
# https://github.com/dabeaz/python-cookbook/blob/master/src/9/defining_a_decorator_that_takes_an_optional_argument/example.py
def auto_register_blueprints(f=None, **options):
  """Automagically register all blueprint packages."""
  import functools
  def decorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
      app, __attr_name__ = f(*args, **kwargs), options.get('attr', 'blueprint'), 
      __func__ = getattr(app, options.get('meth', 'register_blueprint'))
      if __attr_name__:
        import importlib
        import os
        for _ in [ _ for _ in os.listdir('.') if not _[0]=='_' and not _[0]=='.']:
          for path, subdirs, files in os.walk(_):
            for __ in [ _[:-3] for _ in files if not _[0]=='_' and not _[0]=='.' and _[-3:]=='.py']:
              try:
                mod = importlib.import_module(os.path.join(path, __).replace('\\', '.').replace('/', '.'))
              except (ModuleNotFoundError, ImportError, AttributeError) as exc:
                print(f'>>> Failed to load: {exc}!')
              else:
                if hasattr(mod, __attr_name__):
                  __func__(getattr(mod, __attr_name__))
                  print(f'>>> Loaded {__attr_name__}: ', getattr(mod, __attr_name__).name, '|', mod.__name__.split('.')[-2], f'({mod.__name__})')
      return app
    return wrapper
  if f: return decorator(f)
  return decorator#functools.partial(auto_register_blueprints, options=options)

'''
def html_tag_generator(tag, attrs):
  def decorator(func):
    import functools
    @functools.wraps(func)
    def wrapper(text):
      attr_string = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
      return func(f'<{tag} {attr_string}>{text}</{tag}>')
    return wrapper
  return decorator

@html_tag_generator(tag='div', attrs={'class': 'container col-s-12', 'id': 'mydiv'})
def modify_text(text):
  """<- `text` has been modified by the decorator!"""
  print(text)

modify_text('Python')
>><div class='container col-s-12' id='mydiv'>Python</div>
'''