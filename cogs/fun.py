import discord
from discord.ext import commands

from random import randint


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['random'], description='generates a random number in the range minimum (inclusive) - maximum (inclusive)')
	async def rng(self, ctx, minimum: int, maximum: int):
		await ctx.send(randint(minimum, maximum))


def setup(bot):
	bot.add_cog(Fun(bot))
