import discord
from discord.ext import commands

import json


class Counting(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		try:
			with open('counting.json', 'r') as f:
				pass
		except:
			with open('counting.json', 'w+') as f:
				json.dump({}, f, indent=4)

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author.bot:
			return

		try:
			if 'counting' not in msg.channel.name:
				return
		except AttributeError:
			return

		if msg.content.split(' ')[0].isdigit():
			pass
		else:
			return

		with open('counting.json', 'r') as f:
			data = json.load(f)

		if str(msg.guild.id) not in data:
			data[str(msg.guild.id)]	= 1
			with open('counting.json', 'w') as f:
				json.dump(data, f, indent=4)

		try:
			num = int(msg.content.split(' ')[0])
		except:
			return
		
		current_num = int(data[str(msg.guild.id)])

		if num == current_num:
			await msg.add_reaction('✅')
			data[str(msg.guild.id)]	= data[str(msg.guild.id)] + 1
			with open('counting.json', 'w') as f:
				json.dump(data, f, indent=4)
		else:
			data[str(msg.guild.id)]	= 1
			with open('counting.json', 'w') as f:
				json.dump(data, f, indent=4)
			await msg.channel.send(f'wrong number! the counter has been reset to 1')

	@commands.command(description='Displays the current number for this server')
	async def currentnum(self, ctx):
		with open('counting.json', 'r') as f:
			data = json.load(f)

		current_num = data[str(ctx.guild.id)]
		await ctx.send(f'current number: {current_num}')


def setup(bot):
	bot.add_cog(Counting(bot))
