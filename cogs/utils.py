import discord
from discord.ext import commands, tasks


class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.update_activity.start()

	def cog_unload(self):
		self.update_activity.cancel()

	@tasks.loop(seconds=60*5)
	async def update_activity(self):
		activity = f'{self.bot.default_prefixes[0]}help | in {len(self.bot.guilds)} servers'
		await self.bot.change_presence(activity=discord.Game(activity))

	@update_activity.before_loop
	async def before_activity(self):
		await self.bot.wait_until_ready()


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			return

		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(f'error: `{error}`')
			return

		if isinstance(error, commands.BadArgument):
			await ctx.send(f'error: `{error}`')
			return

		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(f'{ctx.author.mention}, you have to wait {round(error.retry_after, 2)} seconds before using this again')
			return

		raise error


def setup(bot):
	bot.add_cog(Utils(bot))
