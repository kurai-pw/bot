from string import ascii_lowercase, ascii_uppercase
from starlette.config import Config

env = Config('.env')

# List of cogs.
MODULES = (
    'events',
    'staff',
    'verification',
    'score_post',
)

DATABASE_CREDENTIALS = {
    'host': env('DATABASE_HOST'),
    'user': env('DATABASE_USER'),
    'pass': env('DATABASE_PASSWORD'),
    'database': env('DATABASE_NAME'),
}

OSU_DOMAIN = env('OSU_DOMAIN')

# Discord data.
GUILD_ID = env('GUILD_ID')

VERIFIED_ROLE_ID = env('VERIFIED_ROLE_ID')
RESTRICTED_ROLE_ID = env('RESTRICTED_ROLE_ID')

# Pattern of verification code.
CODE_PATTERN = ''.join([ascii_lowercase, ascii_uppercase])

MODS = {
    # Mods.
    'first_part': {
        'vn': 0, # Vanilla
        'rx': 4, # Relax
        'ap': 8, # Autopilot
    },
    # Mode.
    'second_part': {
        'std':   0, # osu! standart
        'taiko': 1,
        'catch': 2,
        'mania': 3,
    }
}

AVAILABLE_MODS = [
    'vn!std',
    'vn!taiko',
    'vn!catch',
    'vn!mania',
    'rx!std',
    'rx!taiko',
    'rx!catch',
    'rx!mania',
    'ap!std',
    'ap!taiko',
    'ap!catch',
    'ap!mania',
]

# Guild with those emojis - https://discord.gg/cAzFTTbEQW
GRADE_EMOJI = {
    'X': '<:SSH:1084256202130722866>',
    'SS': '<:SS:1084256199542849596>',
    'SH': '<:SH:1084256197756068001>',
    'S': '<:S_:1084256196900421732>',
    'A': '<:A_:1084256189711396905>',
    'B': '<:B_:1084256192194424924>',
    'C': '<:C_:1084256193477873815>',
    'F': '<:D_:1084256194803290203>',
}

# Guild with those emojis - https://discord.gg/cAzFTTbEQW
SCORE_EMOJI = {
    'n300': '<:hit300:1084280333966520331>',
    'n100': '<:hit100:1084280332938903673>',
    'n50': '<:hit50:1084280331668041788>',
    'miss': '<:hit0:1084280329554108436>',
}
