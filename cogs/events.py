import discord

from discord.ext import commands
from redis import StrictRedis
from settings import GUILD_ID, VERIFIED_ROLE_ID, RESTRICTED_ROLE_ID
from random import choice
from services.database import Database
from services.redis_database import Redis


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name='osu!kurai'
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = Database.execute_query(
            "SELECT discord_id, priv "
            "FROM users "
            f"WHERE discord_id = {member.id}",
            res=True
        )
        if data == ():
            return

        guild = await self.bot.fetch_guild(GUILD_ID)
        user = await guild.fetch_member(member.id)

        if data[0]['priv'] == 2:
            role = guild.get_role(int(RESTRICTED_ROLE_ID))
        else:
            role = guild.get_role(int(VERIFIED_ROLE_ID))
        await user.add_roles(role)


async def setup(bot):
    await bot.add_cog(Events(bot))