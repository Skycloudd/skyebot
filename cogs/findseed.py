import discord
from discord.ext import commands

from random import randint


class Findseed(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description='Simulates Minecraft end portal generation')
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def findseed(self, ctx):
		eyes = 0
		for i in range(12):
			if randint(0, 99) < 10:
				eyes += 1

		await ctx.send(f'{ctx.author.mention} -> your seed is a {eyes} eye')

	@commands.command(aliases=['fsv', 'findseedvisual', 'visualfindseed'], description='Simulates Minecraft end portal generation with graphics')
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def findseedbutvisual(self, ctx):
		portals = []
		eyes = 0
		for i in range(12):
			if randint(0, 99) < 10:
				portals.append('O')
				eyes += 1
			else:
				portals.append('x')

		output = ''
		output += '```\n'
		output += f' {portals[0]}{portals[1]}{portals[2]}\n'
		output += f'{portals[11]}{' '*3}{portals[3]}\n'
		output += f'{portals[10]}{' '*3}{portals[4]}\n'
		output += f'{portals[9]}{' '*3}{portals[5]}\n'
		output += f' {portals[8]}{portals[7]}{portals[6]}\n'
		output += '\n```\n'
		output += f'Your seed is a {eyes} eye'

		await ctx.send(output)


def setup(bot):
	bot.add_cog(Findseed(bot))
