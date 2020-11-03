from bot import SkyeBot
import logging


def setup_logging():
	FORMAT = '%(asctime)s - [%(levelname)s]: %(message)s'
	DATE_FORMAT = '%d/%m/%Y (%H:%M:%S)'

	logger = logging.getLogger('discord')
	logger.setLevel(logging.ERROR)

	file_handler = logging.FileHandler(filename='discord.log', mode='a', encoding='utf-8')
	file_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
	file_handler.setLevel(logging.ERROR)
	logger.addHandler(file_handler)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
	console_handler.setLevel(logging.ERROR)
	logger.addHandler(console_handler)


def run_bot():
	bot = SkyeBot()
	bot.run()


if __name__ == "__main__":
	setup_logging()
	run_bot()
