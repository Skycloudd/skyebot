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

		try:
			with open('listeners.json', 'r') as f:
				pass
		except:
			with open('listeners.json', 'w+') as f:
				json.dump({}, f, indent=4)

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		with open('listeners.json', 'r') as f:
			data = json.load(f)

		try:
			for phrase in data[str(message.guild.id)]:
				if phrase in message.content.lower():
					await message.channel.send(data[str(message.guild.id)][phrase])
		except KeyError:
			return

	@commands.command(description=f'Adds a phrase to react to. Wrap the phrase in quotes: \"phrase here\" to include anything with spaces', aliases=['listener', 'addphrase', 'phrase'])
	async def addlistener(self, ctx, phrase, *, reaction):
		with open('listeners.json', 'r') as f:
			data = json.load(f)

		if str(ctx.guild.id) not in data:
			data[str(ctx.guild.id)] = {}

		if phrase and reaction:
			data[str(ctx.guild.id)][phrase] = reaction
		else:
			return

		with open('listeners.json', 'w') as f:
			json.dump(data, f, indent=4)

		await ctx.send(f'**Added a listener**\n*Phrase*\n\"{phrase}\"\n*Reaction*\n\"{reaction}\"')

	@commands.command(description='Removes a phrase to react to.', aliases=['removephrase'])
	async def removelistener(self, ctx, *, phrase):
		with open('listeners.json', 'r') as f:
			data = json.load(f)

		try:
			data[str(ctx.guild.id)].pop(phrase)
		except KeyError:
			await ctx.send(f'The phrase {phrase} could not be found')
			return

		with open('listeners.json', 'w') as f:
			json.dump(data, f, indent=4)

		await ctx.send(f'Removed phrase \"{phrase}\"')


	@commands.command(aliases=['slotmachine'], description='Simulates a slot machine')
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def slots(self, ctx, show_odds = None):
		items = ['💰', '💎', '🎰', '💵', '🎲', '🏆', '🏅']

		perfect_coins = 100
		high_coins = 50
		medium_coins = 10
		low_coins = -25


		if show_odds != None:
			items_amount = len(items)
			total_options = items_amount**3

			perfect_coins_odds = items_amount * 1 * 1
			perfect_coins_odds /= total_options

			high_coins_odds = (items_amount * 1 * (items_amount - 1) / total_options) + (items_amount * (items_amount - 1) * 1 / total_options)

			medium_coins_odds = items_amount * (items_amount - 1) * 1
			medium_coins_odds /= total_options

			low_coins_odds = items_amount * (items_amount - 1) * (items_amount - 2)
			low_coins_odds /= total_options

			expected = perfect_coins * perfect_coins_odds + high_coins * high_coins_odds + medium_coins * medium_coins_odds + low_coins * low_coins_odds

			output = ''
			output += f'**{perfect_coins} coins**\n{round(perfect_coins_odds * 100, 5)}%\n'
			output += f'**{high_coins} coins**\n{round(high_coins_odds * 100, 5)}%\n'
			output += f'**{medium_coins} coins**\n{round(medium_coins_odds * 100, 5)}%\n'
			output += f'**{low_coins} coins**\n{round(low_coins_odds * 100, 5)}%\n\n'

			output += f'**Expected outcome**\n{round(expected, 5)} coins'

			await ctx.send(output)
			return

		with open('slots.json', 'r') as f:
			data = json.load(f)

		if str(ctx.author.id) not in data:
			data[str(ctx.author.id)] = {"balance": 100, "gamesplayed": 0}

		slots = []

		for i in range(3):
			slots.append(choice(items))

		output = ''
		output += f'{slots[0]} | {slots[1]} | {slots[2]}\n'

		if slots[0] == slots[1] and slots[1] == slots[2]:
			coins = perfect_coins
		elif slots[0] == slots[1] or slots[1] == slots[2]:
			coins = high_coins
		elif slots[0] == slots[2]:
			coins = medium_coins
		else:
			coins = low_coins

		output += f'{coins} coins\n'

		data[str(ctx.author.id)]["balance"] += coins
		output += f'{ctx.author.mention}, your balance is now {data[str(ctx.author.id)]["balance"]} coins\n'

		data[str(ctx.author.id)]["gamesplayed"] += 1
		output += f'You have played {data[str(ctx.author.id)]["gamesplayed"]} games'

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
