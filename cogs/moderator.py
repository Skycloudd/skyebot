import discord
from discord.ext import commands

import asyncio
import json


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_mod(ctx):
        return ctx.author.guild_permissions.manage_channels

    @commands.command(
        description="Bans a user from the server for an amount of time (0 minutes = permanent)"
    )
    @commands.check(is_mod)
    async def ban(
        self,
        ctx,
        user: discord.User,
        minutes: int = 0,
        *,
        reason: str = "No reason provided",
    ):
        if minutes == 0:
            try:
                await user.send(
                    f"You have been permanently banned from {ctx.guild.name}.\nReason: `{reason}`"
                )
            except:
                pass

            await ctx.guild.ban(user, reason=reason, delete_message_days=0)
            await ctx.send(
                f"Banned {user.name} from this server permanently.\nReason: `{reason}`"
            )

        else:
            try:
                await user.send(
                    f"You have been banned from {ctx.guild.name} for {minutes} minutes.\nReason: `{reason}`"
                )
            except:
                pass

            await ctx.guild.ban(user, reason=reason, delete_message_days=0)
            await ctx.send(
                f"Banned {user.name} from this server for {minutes} minutes.\nReason: `{reason}`"
            )
            await asyncio.sleep(minutes * 60)
            await ctx.guild.unban(user, reason=f"Time is up ({minutes} minutes)")

    @commands.command(description="Kicks a user from the server")
    @commands.check(is_mod)
    async def kick(
        self, ctx, user: discord.User, *, reason: str = "No reason provided"
    ):
        try:
            await user.send(
                f"You have been kicked from {ctx.guild.name}.\nReason: `{reason}`"
            )
        except:
            pass

        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"Kicked {user.name} from this server.\nReason: `{reason}`")


def setup(bot):
    bot.add_cog(Moderator(bot))
