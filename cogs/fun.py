import discord
from discord.ext import commands

from random import randint
import json


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['random'], description='Generates a random number in the range minimum (inclusive) - maximum (inclusive)')
	async def rng(self, ctx, minimum: int, maximum: int):
		await ctx.send(randint(minimum, maximum))

	@commands.command(description='Get a random trivia question', aliases=['quiz'])
	async def trivia(self, ctx):
		async with self.bot.session.get(
			"http://jservice.io/api/random"
		) as url:
			data = json.loads(await url.text())

		invalid = data[0]["invalid_count"]

		question = data[0]["question"]
		answer = data[0]["answer"]
		category = data[0]["category"]
		category_title = category["title"]

		embed = discord.Embed(
			title=f'Question: {question}',
			colour=self.bot.main_colour,
			description=f'Category: {category_title}'
		)

		if invalid:
			embed.add_field(
				name='⚠️ Potentially invalid question ⚠️',
				value=f'this question might rely on images or sounds to be answered, based on a count of {invalid}',
				inline=False
			)

		embed.add_field(
			name='Answer',
			value=f'||{answer}||',
			inline=False
		)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Fun(bot))
