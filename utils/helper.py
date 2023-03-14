from re import sub

from services.database import Database

from settings import MODS
from constants.mods import Mods

def mode_from_str(mode: str):
    """
    Converts str modes like vn!std to number.
    """
    try:
        mode, mods = mode.split('!')
        if not mode or not mods:
            raise Exception
        return MODS['first_part'][mode] + MODS['second_part'][mods]
    except:
        return None

def parse_discord_mention(mention: str):
    """
    Try to parse Discord ID from given mention.
    """
    discord_id = sub(r'[^\d\.]', '', mention)

    if len(discord_id) in range(18, 21):
        return discord_id

def get_player_id_by_discord_id(discord_id):
    return Database.execute_query(
        'SELECT `id` '
        'FROM `users` '
        f'WHERE `discord_id` = {discord_id}',
        res=True
    )

def get_player_id_by_name(name):
    return Database.execute_query(
        'SELECT `id` '
        'FROM `users` '
        f'WHERE `safe_name` = "{name}"',
        res=True
    )
