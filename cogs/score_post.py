import nextcord

from nextcord import slash_command, SlashOption
from nextcord.ext import commands

from requests import get
from json import loads
from humanize import intcomma
from time import time

from services.database import Database
from utils.helper import (
    mode_from_str,
    parse_discord_mention,
    get_player_id_by_discord_id,
    get_player_id_by_name
)
from settings import (
    AVAILABLE_MODS,
    GUILD_ID,
    GRADE_EMOJI,
    SCORE_EMOJI,
)

from settings import OSU_DOMAIN
from constants.mods import Mods


class ScorePost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='rs', guild_ids=[GUILD_ID])
    async def recent_score(
        self,
        interaction: nextcord.Interaction,
        mode: str = SlashOption(
            name="mode",
            description='osu! modes.',
            choices=AVAILABLE_MODS,
            default='vn!std',
        ),
        player: str = SlashOption(
            name="player",
            description='Mention player or osu! nickname.',
            default=None,
        )
    ):
        player_id, pp_data = None, None

        converted_mode = mode_from_str(mode)
        if converted_mode is None or converted_mode not in range(0, 12):
            return await interaction.response.send_message('Selected wrong modes, available modes - `vn!std`, `vn!taiko`, `vn!catch`, `vn!mania`, `rx!std`, `rx!taiko`, `rx!catch`, `rx!mania`, `ap!std`, `ap!taiko`, `ap!catch`, `ap!mania`.')

        if player:
            # Try to get player Discord ID if given discord mention.
            player_id = parse_discord_mention(player)

            if player_id:
                player_id = get_player_id_by_discord_id(player_id)
            else:
                # Try to search player in osu! server if given player in-game name.
                player = player.lower()
                player_id = get_player_id_by_name(player)
        else:
            player_id = get_player_id_by_discord_id(interaction.user.id)

        if not player_id:
            return await interaction.response.send_message(
                'Couldn\'t find player, if you sure that a mistake, please contact our developer.'
            )

        player_id = player_id[0]['id']

        request_url = f'https://api.{OSU_DOMAIN}/v1/get_player_scores?id={player_id}&scope=recent&limit=1'
        if mode:
            request_url += f'&mode={converted_mode}'
        data = get(request_url)

        if data.status_code != 200:
            if get(f'https://api.{OSU_DOMAIN}/v1/get_player_count').status_code != 200:
                return await interaction.response.send_message('Get critical error, seems like osu! server is down.')
            return await interaction.response.send_message('Couldn\'t find any score.')

        score_data = loads(data.text)

        score = score_data['scores'][0]
        beatmap = score['beatmap']
        mods = Mods(score['mods']).human_readable()

        # Loads beatmap pp's for different acc's if score isn't SS.
        if not score['perfect']:
            request_pp_data = get(f'https://api.{OSU_DOMAIN}/v1/get_score_pp_range?sid={score["id"]}')

            if request_pp_data.status_code == 200:
                if (data := loads(request_pp_data.text))['status'] == 'success':
                    pp_data = data

        embed = nextcord.Embed(
            color=0xb873be,
            description=
            f"""
            • **{GRADE_EMOJI[score['grade']]}** • **{round(score['pp'], 2)}pp**
            • {round(score['acc'], 2)}%
            • {intcomma(score['score'])} • x{score['max_combo']} / {beatmap['max_combo']}
            • {SCORE_EMOJI['n300']} {score['n300'] + score['ngeki']} • {SCORE_EMOJI['n100']} {score['n100'] + score['nkatu']} • {SCORE_EMOJI['n50']} {score['n50']} • {SCORE_EMOJI['miss']} {score['nmiss']} 
            """,
        ).set_thumbnail(
            url=f'https://assets.ppy.sh/beatmaps/{beatmap["set_id"]}/covers/list.jpg?{time()}'
        ).set_author(
            name=f"{beatmap['title']} ( {beatmap['version']} ){mods} {round(beatmap['diff'], 2)}☆",
            icon_url=f'https://a.{OSU_DOMAIN}/{player_id}?{time()}',
            url=f'https://osu.ppy.sh/b/{beatmap["set_id"]}',
        )

        if pp_data:
            embed.add_field(
                name='FC',
                value='\n'.join([
                    f'**{pp}%** - {round(ranges["performance"], 2)}pp'
                    for pp, ranges in pp_data['pp'].items()
                ]),
                inline=False,
            )

        map_top_data = get(f'https://api.{OSU_DOMAIN}/v1/get_map_scores?scope=best&id={beatmap["id"]}')
        if map_top_data.status_code == 200:
            map_top = loads(map_top_data.text)
            if map_top['status'] == 'success':
                top = None
                for i, bmap_score in enumerate(map_top['scores']):
                    if (bmap_score['userid'] == player_id) and (bmap_score['id'] == score['id']):
                        top = i + 1

                if top:
                    embed.set_footer(
                        text=f'#{top} top',
                        icon_url=interaction.user.avatar.url,
                    )

        await interaction.response.send_message(embed=embed)

def setup(bot) -> None:
    bot.add_cog(ScorePost(bot))