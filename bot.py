import discord
from discord.ext import commands

import json
import time
from aiohttp import ClientSession


extensions = [
	#owner
	'cogs.admin',
	'cogs.utils',
	#normal users
	'cogs.counting',
	'cogs.findseed',
	'cogs.fun',
	'cogs.general',
	'cogs.logs',
	'cogs.moderator',
	'cogs.reactionroles',
	'cogs.starboard'
]

default_prefixes = [',']
def get_prefix(bot, message):
	return commands.when_mentioned_or(*default_prefixes)(bot, message)

intents = discord.Intents.default()
intents.members = True


class SkyeBot(commands.Bot):

	def __init__(self):
		super().__init__(
			command_prefix=get_prefix,
			case_insensitive=True,
			allowed_mentions=discord.AllowedMentions(
				everyone=True,
				users=True,
				roles=True
			),
			intents=intents
		)

		for extension in extensions:
			self.load_extension(extension)

		with open('config.json', 'r') as f:
			self.config = json.load(f)

		self.start_time = time.time()
		self.main_colour = discord.Colour(0xc500ff)
		self.default_prefixes = default_prefixes

		self.session = ClientSession()

	async def on_ready(self):
		print(f'logged in as {self.user}')

		self.appinfo = await self.application_info()
		self.owner = self.appinfo.owner

	async def on_message(self, msg):
		if msg.author.bot:
			return

		await self.process_commands(msg)

	def run(self):
		super().run(self.config['token'], reconnect=True)
