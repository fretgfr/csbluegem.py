import asyncio
from typing import Any

import discord
from discord.ext import commands

import csbluegem

intents = discord.Intents.default()
intents.message_content = True


# This method should be preferred, as it allows for proper
# cleanup of the various resources that are used by csbluegem.py
class MyBot(commands.Bot):
    def __init__(self, prefix: str, csbluegem_client: csbluegem.Client, **options: Any) -> None:
        super().__init__(prefix, **options)
        self.csbluegem_client = csbluegem_client

    async def setup_hook(self):
        # Load extensions, etc.
        ...


async def main():
    # Basic logging setup, can be removed
    # to implement your own behavior.
    discord.utils.setup_logging()

    # 3.9+ syntax
    async with (
        csbluegem.Client() as csbluegem_client,
        MyBot("?", csbluegem_client=csbluegem_client, intents=intents) as bot,
    ):
        await bot.start("YOUR DISCORD TOKEN")


if __name__ == "__main__":
    asyncio.run(main())
