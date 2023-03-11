import json

import discord
from discord.ext import commands

from requests import get
from json import load

from settings import OSU_DOMAIN

from services.database import Database


class ScorePost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rs'])
    async def recent_score(self, ctx: commands.Context):
        player_id = Database.execute_query(
            'SELECT `id` '
            'FROM `users` '
            f'WHERE `discord_id` = {ctx.author.id}',
            res=True
        )
        if not player_id:
            return await ctx.send('Couldn\'t find your Discord ID, please contact our developer.')
        player_id = player_id[0]['id']

        data = get(f'https://api.{OSU_DOMAIN}/v1/get_player_scores?id={player_id}&scope=recent&limit=1')

        if data.status_code != 200:
            if get(f'https://api.{OSU_DOMAIN}/v1/get_player_count').status_code != 200:
                return await ctx.send('Get critical error, seems like osu! server is down.')
            return await ctx.send('Couldn\'t find any score.')

        data = load(data.raw)

        score = data['scores'][0]
        beatmap = score['beatmap']

        await ctx.send(embed=discord.Embed(
            color=0xb873be,
            title=f"{beatmap['title']}"
        ))

async def setup(bot) -> None:
    await bot.add_cog(ScorePost(bot))