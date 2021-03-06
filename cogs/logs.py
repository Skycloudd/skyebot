import discord
from discord.ext import commands

import json


class Logs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		try:
			with open('logs_config.json', 'r') as f:
				pass
		except:
			with open('logs_config.json', 'w+') as f:
				json.dump({}, f, indent=4)

	async def is_mod(ctx):
		try:
			return ctx.author.guild_permissions.manage_channels
		except AttributeError:
			return False

	@commands.group()
	async def logs(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid command passed')

	@commands.check(is_mod)
	@logs.command(description='Sets the channel for message logging')
	async def channel(self, ctx, channel: discord.TextChannel = None):
		if not channel:
			with open('logs_config.json', 'r') as f:
				logs_config = json.load(f)

			logs_config.pop(str(ctx.guild.id), None)

			with open('logs_config.json', 'w') as f:
				json.dump(logs_config, f, indent=4)

			await ctx.send('Message logging has been disabled.')
			return

		if channel.guild.id != ctx.guild.id:
			return

		with open('logs_config.json', 'r') as f:
			logs_config = json.load(f)

		logs_config[str(ctx.guild.id)] = channel.id

		with open('logs_config.json', 'w') as f:
			json.dump(logs_config, f, indent=4)

		await ctx.send(f'Set message logging channel to {channel.mention}')

	@commands.is_owner()
	@logs.command(description='Adds this server to DM logging', aliases=['dm', 'dms'])
	async def dmlogs(self, ctx):
		with open('logs_config.json', 'r') as f:
			logs_config = json.load(f)

		if "dmlogs" not in logs_config:
			logs_config["dmlogs"] = []

		if str(ctx.guild.id) not in logs_config["dmlogs"]:
			logs_config["dmlogs"].append(str(ctx.guild.id))
			await ctx.send(f'Added `{ctx.guild.name}` to DM logs.')
		else:
			logs_config["dmlogs"].remove(str(ctx.guild.id))
			await ctx.send(f'Removed `{ctx.guild.name}` from DM logs.')

		with open('logs_config.json', 'w') as f:
			json.dump(logs_config, f, indent=4)


	@commands.Cog.listener()
	async def on_message_delete(self, msg):

		with open('logs_config.json', 'r') as f:
			logs_config = json.load(f)
		try:
			if str(msg.guild.id) in logs_config["dmlogs"]:
				embed = discord.Embed(
					title='Deleted Message',
					color=self.bot.main_colour,
					timestamp=msg.created_at
				)
				embed.add_field(name='Server', value=msg.guild.name, inline=True)
				embed.add_field(name='User', value=msg.author.mention, inline=True)
				embed.add_field(name='Channel', value=msg.channel.mention, inline=True)
				embed.add_field(name='Message', value=msg.content, inline=False)

				try:
					await self.bot.owner.send(embed=embed)
				except:
					pass
		except AttributeError:
			return

		try:
			channel = self.bot.get_channel(int(logs_config[str(msg.guild.id)]))
		except KeyError:
			return
		except AttributeError:
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
			if str(before.guild.id) in logs_config["dmlogs"]:
				embed = discord.Embed(
					title='Edited Message',
					color=self.bot.main_colour,
					timestamp=after.edited_at
				)
				embed.add_field(name='Server', value=before.guild.name, inline=True)
				embed.add_field(name='User', value=before.author.mention, inline=True)
				embed.add_field(name='Channel', value=before.channel.mention, inline=True)
				embed.add_field(name='Original Message', value=before.content, inline=False)
				embed.add_field(name='New Message', value=after.content, inline=False)

				try:
					await self.bot.owner.send(embed=embed)
				except:
					pass
		except AttributeError:
			return

		try:
			channel = self.bot.get_channel(int(logs_config[str(after.guild.id)]))
		except KeyError:
			return
		except AttributeError:
			return

		if before.author == self.bot.user and before.channel == channel:
			try:
				await channel.send(embed=before.embeds[0])
			except IndexError:
				return
			return

		try:
			embed = discord.Embed(
				title='Edited Message',
				color=self.bot.main_colour,
				timestamp=after.edited_at
			)
		except TypeError:
			return

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
