import discord
from discord.ext import commands

from random import randint
import json
import pokebase as pb


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description='Defines a term with Urban Dictionary', aliases=['urban'])
	async def urbandefine(self, ctx, *, term):
		async with self.bot.session.get(
			f"http://api.urbandictionary.com/v0/define?term=\"{term}\""
		) as url:
			data = json.loads(await url.text())

		embed = discord.Embed(
			title=f'Urban Dictionary definitions for "{term}"',
			colour=self.bot.main_colour
		)

		try:
			top_definition_permalink = data["list"][0]["permalink"]
		except:
			pass

		for entry in data["list"]:
			word = entry["word"]
			definition = entry["definition"]
			example = entry["example"]
			thumbs_up = entry["thumbs_up"]
			thumbs_down = entry["thumbs_down"]
			author = entry["author"]
			permalink = entry["permalink"]

			embed.add_field(
				name=f'Definition for `{word}` by `{author}`',
				value=f'[Link to this definition]({permalink})\n\nDefinition: {definition}\nExample: {example}\n\n👍 {thumbs_up}\n\n👎{thumbs_down}',
				inline=False
			)

		try:
			await ctx.send(embed=embed)
		except:
			await ctx.send(embed=discord.Embed(
				title=f'Urban Dictionary definitions for "{term}"',
				colour=self.bot.main_colour,
				description=f'An error occured. The definitions can be found [here]({top_definition_permalink})'
			))


	@commands.command(description='Gets the base stats for any pokemon')
	async def stats(self, ctx, name):
		try:
			pokemon = pb.pokemon(name)

			embed = discord.Embed(
				title=f'Base stats for {pokemon.name}',
				colour=self.bot.main_colour
			)

			for stat in pokemon.stats:
				embed.add_field(
					name=stat.stat.name,
					value=stat.base_stat
				)

			await ctx.send(embed=embed)
		except AttributeError:
			await ctx.send(f'The pokemon `{name}` doesn\'t exist!')
			return

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

	@commands.command(description='Get the \"Astronomy Picture of the Day\" from NASA', aliases=['apod'])
	async def nasapic(self, ctx):
		apikey = self.bot.config["nasa_apikey"]

		async with self.bot.session.get(
			f'https://api.nasa.gov/planetary/apod?api_key={apikey}'
		) as url:
			data = json.loads(await url.text())

		hd_url = data["hdurl"]
		title = data["title"]
		explanation = data["explanation"]
		date = data["date"]
		try:
			copyright = data["copyright"]
		except KeyError:
			copyright = None

		embed = discord.Embed(
			title=f'NASA Astronomy Picture of the Day',
			colour=self.bot.main_colour,
			description=f'{explanation}'
		)

		if copyright:
			embed.set_author(name=copyright)

		embed.set_image(url=hd_url)

		embed.set_footer(text=date)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Fun(bot))
