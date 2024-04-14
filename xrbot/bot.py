"""Module responsible for starting the bot and loading the commands"""

from __future__ import annotations

import asyncio
import os
import sys
from dotenv import load_dotenv

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotFound, NoEntryPointError

initial_extensions = [
    "cogs.help",
    "cogs.reddit",
    "cogs.webscraping",
    "cogs.flag_guesser",
]

intents = discord.Intents.all()

BOT_PREFIX = "x!"


class Xrbot(commands.Bot):
    """Bot class for the bot

    Args:
        commands (discord.Bot): The bot object
    """

    debug: bool
    bot_app_info: discord.AppInfo

    def __init__(self) -> None:
        super().__init__(
            command_prefix=BOT_PREFIX, case_insensitive=True, intents=intents
        )
        self.session: aiohttp.ClientSession = None
        self.bot_version = "2.0.0"

    async def load_cogs(self) -> None:
        """Load the cogs (extensions) for the bot"""
        for ext in initial_extensions:
            try:
                await self.load_extension(ext)
            except (
                ExtensionNotFound,
                ExtensionFailed,
                NoEntryPointError,
            ) as e:
                print(e)
                print(f"Failed to load extension {ext}.", file=sys.stderr)

    async def setup_hook(self) -> None:
        """Setup the bot and load extensions (cogs)"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

        await self.load_cogs()

    async def on_ready(self) -> None:
        """Called when the bot is ready"""
        await self.tree.sync()
        print(f"We have logged in as {self.user}")
        print(f"Version: {self.bot_version}")

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Learn Hebrew while sleeping 8h version",
            )
        )

    async def close(self) -> None:
        """Close the bot and the aiohttp session"""
        await self.session.close()
        await super().close()

    async def start(self, debug: bool = False) -> None:
        """Start the bot

        Args:
            debug (bool, optional): Whether to run the bot in debug mode. Defaults to False.

        Returns:
            None
        """
        self.debug = debug
        load_dotenv()
        return await super().start(os.getenv("TOKEN"), reconnect=True)


def run_bot() -> None:
    """Run the bot"""
    bot = Xrbot()
    asyncio.run(bot.start())
