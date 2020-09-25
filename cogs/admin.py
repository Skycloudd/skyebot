import discord
from discord.ext import commands

import git
import os


class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.is_owner()
	@commands.command(aliases=['quit', 'exit'])
	async def forceexit(self, ctx):
		await ctx.send(f'bot force-exited by {ctx.author.mention}')
		exit(0)

	@commands.is_owner()
	@commands.command()
	async def pull(self, ctx):
		g = git.cmd.Git(os.getcwd())
		await ctx.send(f'Probably pulled.\n```bash\n{g.pull()}```')

	@commands.is_owner()
	@commands.command(name='reload', usage='<extension>')
	async def _reload(self, ctx, ext):
		try:
			self.bot.reload_extension(f'cogs.{ext}')
			await ctx.send(f'The extension {ext} was reloaded!')
		except commands.ExtensionNotFound:
			await ctx.send(f'The extension {ext} doesn\'t exist.')
		except commands.ExtensionNotLoaded:
			await ctx.send(f'The extension {ext} is not loaded! (use {ctx.prefix}load)')
		except commands.NoEntryPointError:
			await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function) ')
		except commands.ExtensionFailed:
			await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
			self.bot.logger.exception(f'Failed to reload extension {ext}:')
			
	@commands.is_owner()
	@commands.command(name='load', usage='<extension>')
	async def _load(self, ctx, ext):
		try:
			self.bot.load_extension(f'cogs.{ext}')
			await ctx.send(f'The extension {ext} was loaded!')
		except commands.ExtensionNotFound:
			await ctx.send(f'The extension {ext} doesn\'t exist!')
		except commands.ExtensionAlreadyLoaded:
			await ctx.send(f'The extension {ext} is already loaded.')
		except commands.NoEntryPointError:
			await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function)')
		except commands.ExtensionFailed:
			await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
			self.bot.logger.exception(f'Failed to reload extension {ext}:')

	@commands.is_owner()
	@commands.command(name='unload', usage='<extension>')
	async def _unload(self, ctx, ext):
		try:
			self.bot.unload_extension(f'cogs.{ext}')
			await ctx.send(f'The extension {ext} was unloaded!')
		except commands.ExtensionNotFound:
			await ctx.send(f'The extension {ext} doesn\'t exist!')
		except commands.NoEntryPointError:
			await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function)')
		except commands.ExtensionFailed:
			await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
			self.bot.logger.exception(f'Failed to unload extension {ext}:')

	@commands.is_owner()
	@commands.command()
	async def activity(self, ctx,*, activity=None):
		if activity:
			game = discord.Game(activity)
		else:
			activity = ''
			game = discord.Game(activity)
		await self.bot.change_presence(activity=game)
		await ctx.send(f'Activity changed to {activity}')


def setup(bot):
	bot.add_cog(Admin(bot))
