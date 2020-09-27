import discord
from discord.ext import commands

import time


class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description='Displays information about the bot')
	async def info(self, ctx):
		seconds = time.time() - self.bot.start_time
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		d, h = divmod(h, 24)
		w, d = divmod(d, 7)
		uptime_str = f'{int(w)}w : {int(d)}d : {int(h)}h : {int(m)}m : {int(s)}s'

		embed = discord.Embed(
			title='Information about SkyeBot',
			colour=self.bot.main_colour,
			description='This bot was made by `skye#9250`. The full source code can be found at https://github.com/Skycloudd/skyebot.'
		)

		embed.set_thumbnail(url=self.bot.user.avatar_url_as(format="png"))

		embed.add_field(
			name='Info',
			value=f'ID: {self.bot.user.id}\nName: {self.bot.user.name}',
			inline=True
		)
		embed.add_field(
			name='Bot ping to Discord servers',
			value=f'{round(self.bot.latency * 1000)}ms',
			inline=True
		)
		embed.add_field(
			name='Library',
			value=f'Discord.py v{discord.__version__}',
			inline=True
		)
		embed.add_field(
			name='Uptime',
			value=uptime_str,
			inline=True
		)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(General(bot))
