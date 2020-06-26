
import asyncio

from bot import Bot
from utils.environ import get_env

if __name__ == '__main__':
  bot = Bot()
  try:
  	bot.run(token=get_env('DISCORD_BOT_TOKEN'))
  except Exception as e:
  	print(f'Whoops, bot failed to connect to Discord.\n\n{e}')
