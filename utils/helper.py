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
