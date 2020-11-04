import discord
from discord.ext import commands

import json


class Reactionroles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		try:
			with open('reactionroles.json', 'r') as f:
				pass
		except:
			with open('reactionroles.json', 'w+') as f:
				json.dump({}, f, indent=4)

	async def is_mod(ctx):
		return ctx.author.guild_permissions.manage_channels

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		channel = self.bot.get_channel(payload.channel_id)

		guild = self.bot.get_guild(payload.guild_id)
		member = guild.get_member(payload.user_id)

		message_id = payload.message_id

		emote = payload.emoji

		if member.bot:
			return

		try:
			with open('reactionroles.json', 'r') as f:
				reactionroles = json.load(f)
		except FileNotFoundError:
			return

		try:
			msg = None
			for message in reactionroles[str(guild.id)]["messages"]:
				if message["message_id"] == message_id:
					msg = message
					break
		except KeyError:
			return

		if not msg:
			return
		
		if str(msg["emote"]) != str(emote):
			return

		role = guild.get_role(msg["role_id"])
		if role:
			await member.add_roles(role)

	@commands.command()
	@commands.check(is_mod)
	async def reactionrole(self, ctx, channel: discord.TextChannel, message_id: int, role_id: int, emote: str):
		with open('reactionroles.json', 'r') as f:
			reactionroles = json.load(f)

		if str(ctx.guild.id) not in reactionroles:
			reactionroles[str(ctx.guild.id)] = {}

		if "messages" not in reactionroles[str(ctx.guild.id)]:
			reactionroles[str(ctx.guild.id)]["messages"] = []

		try:
			msg = await channel.fetch_message(message_id)
		except:
			await ctx.send(f'Error: `Couldn\'t find a message with id {message_id} in this channel`')
			return

		try:
			await ctx.message.add_reaction(emote)
			await msg.add_reaction(emote)
		except:
			await ctx.send(f'Error: `{emote} is an invalid emote`')
			return

		role = ctx.guild.get_role(role_id)
		if not role:
			await ctx.send(f'Error: `Couldn\'t find a role with id {role_id} in this server`')
			return

		reactionroles[str(ctx.guild.id)]["messages"].append(
			{
				"message_id": msg.id,
				"emote": emote,
				"role_id": role.id
			}
		)

		with open('reactionroles.json', 'w') as f:
			json.dump(reactionroles, f, indent=4)


def setup(bot):
	bot.add_cog(Reactionroles(bot))
