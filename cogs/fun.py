import discord
from discord.ext import commands

from random import randint, choice
import json
import pokebase as pb
import calendar


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		try:
			with open('slots.json', 'r') as f:
				pass
		except:
			with open('slots.json', 'w+') as f:
				json.dump({}, f, indent=4)

	@commands.command(aliases=['slotmachine'], description='Simulates a slot machine')
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def slots(self, ctx, odds):
		with open('slots.json', 'r') as f:
			data = json.load(f)

		if str(ctx.author.id) not in data:
			data[str(ctx.author.id)] = {"balance": 100}

		items = ['♠', '💰', '💎', '🎰', '💵', '🎲', '🏆', '🏅']

		slots = []

		for i in range(3):
			slots.append(choice(items))

		output = ''
		if slots[0] == slots[1] and slots[1] == slots[2]:
			coins = 100
			output += f'{slots[0]} | {slots[1]} | {slots[2]}\n'
			output += f'{coins} coins\n'
			data[str(ctx.author.id)]["balance"] += coins
			output += f'{ctx.author.mention}, your balance is now {data[str(ctx.author.id)]["balance"]} coins'
		
		elif slots[0] == slots[1] or slots[1] == slots[2]:
			coins = 50
			output += f'{slots[0]} | {slots[1]} | {slots[2]}\n'
			output += f'{coins} coins\n'
			data[str(ctx.author.id)]["balance"] += coins
			output += f'{ctx.author.mention}, your balance is now {data[str(ctx.author.id)]["balance"]} coins'
		
		elif slots[0] == slots[2]:
			coins = 10
			output += f'{slots[0]} | {slots[1]} | {slots[2]}\n'
			output += f'{coins} coins\n'
			data[str(ctx.author.id)]["balance"] += coins
			output += f'{ctx.author.mention}, your balance is now {data[str(ctx.author.id)]["balance"]} coins'	
		
		else:
			coins = -20
			output += f'{slots[0]} | {slots[1]} | {slots[2]}\n'
			output += f'{coins} coins\n'
			data[str(ctx.author.id)]["balance"] += coins
			output += f'{ctx.author.mention}, your balance is now {data[str(ctx.author.id)]["balance"]} coins'

		with open('slots.json', 'w') as f:
			json.dump(data, f, indent=4)

		await ctx.send(output)

	@commands.command(name='calendar', description='Displays the calendar for a given year and month')
	async def calendar_(self, ctx, year: int, month: str):
		try:
			month = int(month)
		except ValueError:
			if month.lower() in (x.lower() for x in calendar.month_name):
				month = list(calendar.month_name).index(month.capitalize())
			elif month.lower() in (x.lower() for x in calendar.month_abbr):
				month = list(calendar.month_abbr).index(month.capitalize())
			else:
				await ctx.send(f'`{month}` is not a valid month')
				return

		cal = calendar.month(year, month)

		embed = discord.Embed(
			title=f'{year} / {calendar.month_name[month]}',
			colour=self.bot.main_colour,
			description=f'```\n{cal}```'
		)

		await ctx.send(embed=embed)

	@commands.command(description='Defines a term with Urban Dictionary', aliases=['urban'])
	async def urbandefine(self, ctx, *, term: str):
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
	async def stats(self, ctx, name: str):
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
			title=title,
			colour=self.bot.main_colour,
			description=explanation
		)

		if copyright:
			embed.set_author(name=copyright)

		embed.set_image(url=hd_url)

		embed.set_footer(text=date)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Fun(bot))
