
from . import BaseConfig
from utils.environ import get_env
class Discord(BaseConfig):
  TOKEN = get_env('DISCORD_BOT_TOKEN', None)
  __prefixes__ = get_env('DISCORD_BOT_PREFIXES', None)
  if __prefixes__:
    __prefixes__ = __prefixes__.split(',')
  PREFIXES = __prefixes__ or ['?', '!', '>', '$']
