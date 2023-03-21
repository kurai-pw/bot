from nextcord import Embed
from nextcord.ext import commands

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int = 1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(
                description = f'** {ctx.author.name}, you dont have permissions.**',
                color=0x0c0c0c
            ))
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(
                description = f'** Wrong arguments.**',
                color=0x0c0c0c
            ))
        else:
            await ctx.send(embed=Embed(
                description=f'** Unhandled exception, try again.**',
                color=0x0c0c0c
            ))


def setup(bot) -> None:
    bot.add_cog(Staff(bot))
