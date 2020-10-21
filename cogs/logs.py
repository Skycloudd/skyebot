import discord
from discord.ext import commands

import json


class Logs(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	async def logs(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid command passed')

	@logs.command()
	async def channel(self, ctx, channel: discord.TextChannel):
		if channel.guild.id != ctx.guild.id:
			return

		with open('logs_config.json', 'r') as f:
			logs_config = json.load(f)

		logs_config[str(ctx.guild.id)] = channel.id

		with open('logs_config.json', 'w') as f:
			json.dump(logs_config, f, indent=4)

		await ctx.send(f'Set message logging channel to {channel.mention}')



	@commands.Cog.listener()
	async def on_message_delete(self, msg):

		with open('logs_config.json', 'r') as f:
			logs_config = json.load(f)

		try:
			channel = self.bot.get_channel(int(logs_config[str(msg.guild.id)]))
		except KeyError:
			return

		if msg.author == self.bot.user and msg.channel == channel:
			try:
				await channel.send(embed=msg.embeds[0])
			except IndexError:
				return
			return


		embed = discord.Embed(
			title='Deleted Message',
			color=self.bot.main_colour,
			timestamp=msg.created_at
		)
		embed.add_field(name='User', value=msg.author.mention, inline=True)
		embed.add_field(name='Channel', value=msg.channel.mention, inline=True)
		embed.add_field(name='Message', value=msg.content, inline=False)

		try:
			await channel.send(embed=embed)
		except:
			return

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if before.content == after.content and len(before.embeds) != len(after.embeds) + 1:
			return

		with open('logs_config.json', 'r') as f:
			logs_config = json.load(f)

		try:
			channel = self.bot.get_channel(int(logs_config[str(after.guild.id)]))
		except KeyError:
			return

		if before.author == self.bot.user and before.channel == channel:
			try:
				await channel.send(embed=before.embeds[0])
			except IndexError:
				return
			return

		embed = discord.Embed(
			title='Edited Message',
			color=self.bot.main_colour,
			timestamp=after.edited_at
		)
		embed.add_field(name='User', value=before.author.mention, inline=True)
		embed.add_field(name='Channel', value=before.channel.mention, inline=True)
		embed.add_field(name='Original Message', value=before.content, inline=False)
		embed.add_field(name='New Message', value=after.content, inline=False)

		try:
			await channel.send(embed=embed)
		except:
			return


def setup(bot):
	bot.add_cog(Logs(bot))
