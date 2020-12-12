import discord
from discord.ext import commands

import json


class Starboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		try:
			with open('starboard_config.json', 'r') as f:
				pass
		except:
			with open('starboard_config.json', 'w+') as f:
				json.dump({}, f, indent=4)

	async def is_mod(ctx):
		try:
			return ctx.author.guild_permissions.manage_channels
		except AttributeError:
			return False

	@commands.group()
	async def starboard(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid command passed')

	@commands.check(is_mod)
	@starboard.command(description='Sets the channel for starboard')
	async def setup(self, ctx, channel: discord.TextChannel = None, amount: int = 5):
		if not channel:
			with open('starboard_config.json', 'r') as f:
				starboard_config = json.load(f)

			starboard_config.pop(str(ctx.guild.id), None)

			with open('starboard_config.json', 'w') as f:
				json.dump(starboard_config, f, indent=4)

			await ctx.send('Starboard has been disabled.')
			return

		if channel.guild.id != ctx.guild.id:
			return

		with open('starboard_config.json', 'r') as f:
			starboard_config = json.load(f)

		if str(ctx.guild.id) not in starboard_config:
			starboard_config[str(ctx.guild.id)] = {}

		starboard_config[str(ctx.guild.id)]["channel"] = channel.id
		starboard_config[str(ctx.guild.id)]["amount"] = amount
		if "pins" not in starboard_config[str(ctx.guild.id)]:
			starboard_config[str(ctx.guild.id)]["pins"] = []

		with open('starboard_config.json', 'w') as f:
			json.dump(starboard_config, f, indent=4)

		await ctx.send(f'**Starboard setup**\nChannel: {channel.mention}\nRequired stars: {amount}')

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		with open('starboard_config.json', 'r') as f:
			starboard_config = json.load(f)

		if (
			reaction.emoji == '⭐'
			and reaction.count >= int(starboard_config[str(reaction.message.guild.id)]["amount"])
			and not reaction.message.id in starboard_config[str(reaction.message.guild.id)]["pins"]
		):
			starboard_config[str(reaction.message.guild.id)]["pins"].append(reaction.message.id)

			with open('starboard_config.json', 'w') as f:
				json.dump(starboard_config, f, indent=4)

			embed = discord.Embed(
				title="**New Starred Message**",
				description=reaction.message.content,
				colour=self.bot.main_colour,
				url=reaction.message.jump_url,
				timestamp=reaction.message.created_at,
			)

			for attachement in reaction.message.attachments:
				if attachement.height:
					embed.set_image(url=attachement.url)
			embed.set_author(
				name=str(reaction.message.author),
				icon_url=reaction.message.author.avatar_url_as(format="png"),
			)
			embed.set_footer(text=reaction.message.id)

			channel = self.bot.get_channel(int(starboard_config[str(reaction.message.guild.id)]["channel"]))
			await channel.send(embed=embed)


def setup(bot):
	bot.add_cog(Starboard(bot))
