import nextcord

from nextcord.ext import commands

from redis import StrictRedis
from random import choice

from services.database import Database
from services.redis_database import Redis

from settings import CODE_PATTERN, GUILD_ID, VERIFIED_ROLE_ID


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        while True:
            code = ''.join([choice(CODE_PATTERN) for _ in range(8)])

            if Redis.get(f'verification:{code}') is None:
                Redis.set(f'verification:{code}', ctx.author.id)
                break

        return await ctx.author.send(embed=nextcord.Embed(
            title='Verification code',
            description=f'Send `!verify {code}` to `kurai.bot`.',
            color=0xb873be,
        ))

    @commands.command()
    async def letme(self, ctx: commands.Context):
        r = StrictRedis()
        for key in r.scan_iter("verification:*"):
            if int(Redis.get(key.decode("utf-8")).decode("utf-8")) == ctx.author.id:
                data = Database.execute_query(
                    "SELECT discord_id "
                    "FROM users "
                    f"WHERE discord_id = {ctx.author.id}",
                    res=True
                )
                if not data or (data[0]['discord_id'] != ctx.author.id):
                    return await ctx.author.send('You\'re not yet verified, please follow instructions.')

                r.delete(key)

                # Add role 'Member' to User.
                guild = await self.bot.fetch_guild(GUILD_ID)
                user = await guild.fetch_member(ctx.author.id)
                role = guild.get_role(int(VERIFIED_ROLE_ID))
                await user.add_roles(role)

                return await ctx.author.send(embed=nextcord.Embed(
                    title='Enjoy!',
                    description='Welcome to **kurai.pw** Discord server!',
                    color=0xb873be,
                ))
        await ctx.author.send(embed=nextcord.Embed(
            description='Could not find data about completed verification process or you\'re already verified.',
            color=0xb873be,
        ))

def setup(bot) -> None:
    bot.add_cog(Verification(bot))
