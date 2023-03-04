from string import ascii_lowercase, ascii_uppercase
from starlette.config import Config

env = Config('.env')

# List of cogs.
MODULES = (
    'verification',
    'events'
)

DATABASE_CREDENTIALS = {
    'host': env('DATABASE_HOST'),
    'user': env('DATABASE_USER'),
    'pass': env('DATABASE_PASSWORD'),
    'database': env('DATABASE_NAME'),
}

GUILD_ID = env('GUILD_ID')
VERIFIED_ROLE_ID = env('VERIFIED_ROLE_ID')
RESTRICTED_ROLE_ID = env('RESTRICTED_ROLE_ID')

# Pattern of verification code.
CODE_PATTERN = ''.join([ascii_lowercase, ascii_uppercase])
