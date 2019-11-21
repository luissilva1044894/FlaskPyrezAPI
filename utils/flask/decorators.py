
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
