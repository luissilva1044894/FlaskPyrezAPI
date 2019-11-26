
from . import Config
class Discord(Config):
	from utils import get_env

	TOKEN = get_env('DISCORD_BOT_TOKEN', None)
	__prefixes__ = get_env('DISCORD_BOT_PREFIXES', None)
	if __prefixes__:
		__prefixes__ = __prefixes__.split(',')
	PREFIXES = __prefixes__ or ['?', '!', '>', '$']
