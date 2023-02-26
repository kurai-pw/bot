import discord

from discord.ext import commands
from redis import StrictRedis
from settings import CODE_PATTERN, GUILD_ID, VERIFIED_ROLE_ID
from random import choice
from services.database import Database
from services.redis_database import Redis


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name='osu!'
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # @TODO Add check if user are verified and or restricted.
        pass

    @commands.command()
    async def code(self, ctx: commands.Context):
        data = Database.execute_query(
            "SELECT discord_id "
            "FROM users "
            f"WHERE discord_id = {ctx.author.id}",
            res=True
        )
        if data != ():
            return await ctx.author.send('You\'re already verified.')

        code = ''.join([choice(CODE_PATTERN) for _ in range(8)])
        Redis.set(f'verification:{code}', ctx.author.id)

        return await ctx.author.send(embed=discord.Embed(
            title='Verification code',
            description=code,
            color=0xb873be,
        ))
        # return await ctx.author.send(f'Verification code  -  `{code}`')




    @commands.command()
    async def letme(self, ctx: commands.Context):
        r = StrictRedis()
        for key in r.scan_iter("verification:*"):
            if Redis.get(f'verification:{key}') == ctx.author.id:
                r.delete(key)

                guild = self.bot.get_guild(GUILD_ID)
                user = guild.get_member(ctx.author.id)
                role = guild.get_role(VERIFIED_ROLE_ID)
                await user.add_roles(role)

async def setup(bot):
    await bot.add_cog(Verification(bot))