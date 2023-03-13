import asyncio

from nextcord import Intents
from nextcord.ext import commands

from starlette.config import Config

from settings import MODULES

env = Config('.env')


async def main():
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or(env('PREFIX')),
        intents=Intents.all(),
        help_command=None
    )

    for module in MODULES:
        bot.load_extension('cogs.' + module)

    await bot.start(env('TOKEN'))


if __name__ == '__main__':
    asyncio.run(main())
