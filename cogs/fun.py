import discord
from discord.ext import commands

from random import randint


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['random'], description='Generates a random number in the range minimum (inclusive) - maximum (inclusive)')
	async def rng(self, ctx, minimum: int, maximum: int):
		await ctx.send(randint(minimum, maximum))

	@commands.command(description='Simulates Minecraft end portal generation')
	async def findseed(self, ctx):
		eyes = 0
		for i in range(12):
			if randint(0, 99) < 10:
				eyes += 1

		await ctx.send(f'{ctx.author.mention} -> your seed is a {eyes} eye')


def setup(bot):
	bot.add_cog(Fun(bot))
