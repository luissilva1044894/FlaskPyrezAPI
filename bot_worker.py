
if __name__ == '__main__':
	import asyncio
	from utils.loop import get_event_loop
	asyncio.set_event_loop(get_event_loop())

	from discord_bot import Bot
	from utils.discord import DiscordConfig
	from utils import get_env
	bot = Bot(config=DiscordConfig())
	bot.run(get_env('DISCORD_BOT_TOKEN', None))
	#from discord_bot import main
	#main()
