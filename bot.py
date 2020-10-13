import discord
from discord.ext import commands

import logging
import json
import time


extensions = [
	#owner
	'cogs.utils',
	'cogs.admin',
	#normal users
	'cogs.moderator',
	'cogs.logs',
	'cogs.general',
	'cogs.fun',
	'cogs.counting',
	'cogs.findseed'
]

default_prefixes = [',']
def get_prefix(bot, message):
	return commands.when_mentioned_or(*default_prefixes)(bot, message)


class SkyeBot(commands.Bot):

	def __init__(self):
		super().__init__(
			command_prefix=get_prefix,
			case_insensitive=True,
			allowed_mentions=discord.AllowedMentions(
				everyone=True,
				users=True,
				roles=True
			)
		)
		self.logger = logging.getLogger('discord')


		for extension in extensions:
			self.load_extension(extension)

		with open('config.json', 'r') as f:
			self.config = json.load(f)

		self.start_time = time.time()
		self.main_colour = discord.Colour(0xc500ff)

	async def on_ready(self):
		print(f'logged in as {self.user}')

		activity = f'{default_prefixes[0]}help'
		await self.change_presence(activity=discord.Game(activity))

	async def on_message(self, msg):
		if msg.author.bot:
			return

		await self.process_commands(msg)

	def run(self):
		super().run(self.config['token'])
