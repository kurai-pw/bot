import discord
import asyncio

from starlette.config import Config
from discord.ext import commands
from settings import MODULES

env = Config('.env')


async def main():
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or(env('PREFIX')),
        intents=discord.Intents.all(),
        help_command=None
    )

    async with bot:
        for module in MODULES:
            await bot.load_extension('cogs.' + module)

        await bot.start(env('TOKEN'))


if __name__ == '__main__':
    asyncio.run(main())
