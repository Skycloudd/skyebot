from discord.ext import commands


class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

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
