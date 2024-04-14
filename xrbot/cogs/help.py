"""Functions of the commands related to the Help features of the bot"""

import discord
from discord.ext import commands
from discord.app_commands import command, describe, choices, Choice, CommandTree
from core.embed_builder import EmbedBuilder


class Help(commands.Cog, name="Help"):
    """Class for Help commands

    Args:
        commands (commands.Cog): The commands object
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    async def all_help(self, interaction: discord.Interaction) -> None:
        """Lists the help command for each module

        Args:
            ctx (discord.Context): Context of command
        """
        embed_builder = EmbedBuilder(
            title=f"All help Commands | {interaction.user}",
            description=" ",
            color=(255, 255, 255),
        )

        fields = [
            {
                "name": "x!help Memo",
                "value": "Shows list of Memo commands & what they do",
            },
            {
                "name": "x!help MiniCommands",
                "value": "Shows list of Mini commands & what they do",
            },
            {
                "name": "x!help FlagGuesser",
                "value": "Shows list of FlagGuesser commands & what they do",
            },
            {
                "name": "x!help TicTacToe",
                "value": "Shows list of TicTacToe commands & what they do",
            },
            {
                "name": "x!help Reddit",
                "value": "Shows list of Reddit commands & what they do",
            },
        ]

        embed_builder.add_bulk_fields(fields)

        try:
            await interaction.response.send_message(embed=embed_builder.build())
        except discord.DiscordException as e:
            print(f"Error sending embed: {e}")

    async def miscellaneous_help(self, interaction: discord.Interaction) -> None:
        """Lists miscellaneous help commands.

        Args:
            ctx (discord.Context): Context of the command
        """
        embed_builder = EmbedBuilder(
            title=f"Miscellaneous Help Commands | {interaction.user}",
            description="Here are the available miscellaneous commands:",
            color=(255, 255, 255),
        )

        fields = [
            {
                "name": "x!get lyrics <artist> <song>",
                "value": "Shows lyrics of <song> by <artist>.",
            },
            {
                "name": "x!get weather <country> <city>",
                "value": "Shows the weather forecast for the next 6 hours in <city>, <country>.",
            },
        ]

        embed_builder.add_bulk_fields(fields)

        try:
            await interaction.respond(embed=embed_builder.build())
        except discord.DiscordException as e:
            print(f"Error sending embed: {e}")

    async def memo_help(self, interaction: discord.Interaction) -> None:
        """Lists memo commands and their descriptions.

        Args:
            ctx (discord.Context): Context of the command
        """
        embed_builder = EmbedBuilder(
            title=f"Memo Commands | {interaction.user}",
            description="Here's a list of memo commands and their usage:",
            color=(255, 245, 93),  # Using a different color for Memo commands
        )

        fields = [
            {
                "name": "x!memo add <memo>",
                "value": "Adds <memo> to your list of memos.",
            },
            {
                "name": "x!memo remove <memo number>",
                "value": "Removes memo at <memo number> from your list.",
            },
            {
                "name": "x!memo view <memo number>",
                "value": "Displays memo at <memo number>.",
            },
            {"name": "x!memo view all", "value": "Displays all your memos."},
        ]

        embed_builder.add_bulk_fields(fields)

        try:
            await interaction.response.send_message(embed=embed_builder.build())
        except discord.DiscordException as e:
            print(f"Error sending embed: {e}")

    async def mini_commands_help(self, interaction: discord.Interaction) -> None:
        """Lists Mini commands and their descriptions.

        Args:
            ctx (discord.Context): Context of the command.
        """
        embed_builder = EmbedBuilder(
            title=f"Mini Commands | {interaction.user}",
            description="Here are the available Mini commands:",
            color=(198, 195, 255),
        )

        fields = [
            {"name": "x!cf", "value": "Flips a coin."},
            {
                "name": "x!move <num> <channel>",
                "value": "Purges the last <num> messages and moves them to <channel>.",
            },
            {"name": "x!purge <num>", "value": "Purges the last <num> messages."},
            {"name": "x!Penguroll", "value": "Shows a random Pengu."},
            {
                "name": "x!random <num1> <num2>",
                "value": "Pick a number between <num1> and <num2>.",
            },
            {
                "name": "x!bs <Participant 1> <Participant 2>... <Participant n>",
                "value": "Spins a bottle and shows who it's pointing to and from.",
            },
            {
                "name": "x!poll <Question> - <option 1> - <option 2> - ... - <option n>",
                "value": "Sends a reaction poll message (max options are 9).",
            },
        ]

        embed_builder.add_bulk_fields(fields)

        try:
            await interaction.response.send_message(embed=embed_builder.build())
        except discord.DiscordException as e:
            print(f"Error sending embed: {e}")

    async def flag_guesser_help(self, interaction: discord.Interaction) -> None:
        """Lists FlagGuesser commands and their descriptions.

        Args:
            ctx (discord.Context): Context of the command.
        """
        embed_builder = EmbedBuilder(
            title=f"FlagGuesser Commands | {interaction.user}",
            description="Here are the available FlagGuesser commands:",
            color=(0, 136, 35),
        )

        fields = [
            {"name": "flagguesser start", "value": "Starts a game of FlagGuesser."},
            {
                "name": "flagguesser guess <number>",
                "value": "Submits country number <number> as your answer.",
            },
            {
                "name": "flagguesser end",
                "value": "Ends the ongoing game of FlagGuesser.",
            },
        ]

        embed_builder.add_bulk_fields(fields)

        try:
            await interaction.response.send_message(embed=embed_builder.build())
        except discord.DiscordException as e:
            print(f"Error sending embed: {e}")

    async def tic_tac_toe_help(self, interaction: discord.Interaction) -> None:
        """Lists TicTacToe commands and their descriptions.

        Args:
            ctx (discord.Context): Context of the command.
        """
        embed_builder = EmbedBuilder(
            title=f"TicTacToe Commands | {interaction.user}",
            description="Here are the available TicTacToe commands:",
            color=(255, 153, 249),
        )

        fields = [
            {
                "name": "x!TicTacToe start <user>",
                "value": "Starts a game of TicTacToe vs <user> or vs the bot if no user specified.",
            },
            {
                "name": "x!tictactoe play <slot #>",
                "value": "Places a piece in slot <slot #>.",
            },
            {"name": "x!accept", "value": "Accepts TicTacToe match request."},
            {"name": "x!reject", "value": "Rejects TicTacToe match request."},
            {"name": "x!TicTacToe end", "value": "Ends ongoing TicTacToe match."},
        ]

        embed_builder.add_bulk_fields(fields)

        try:
            await interaction.response.send_message(embed=embed_builder.build())
        except discord.DiscordException as e:
            print(f"Error sending embed: {e}")

    async def reddit_help(self, interaction: discord.Interaction) -> None:
        """Lists Reddit commands and their descriptions.

        Args:
            ctx (discord.Context): Context of the command.
        """
        embed_builder = EmbedBuilder(
            title=f"Reddit Commands | {interaction.user}",
            description="Here are the available Reddit commands:",
            color=(255, 162, 162),
        )

        fields = [
            {"name": "x!reddit view <username>", "value": "Shows info of Reddit user."},
            {"name": "x!reddit sub <name>", "value": "Shows info of Subreddit."},
            {
                "name": "x!reddit <category> <subreddit> <number>",
                "value": "Shows poster number <number> in <category> of <subreddit>.",
            },
        ]

        embed_builder.add_bulk_fields(fields)

        try:
            await interaction.response.send_message(embed=embed_builder.build())
        except discord.DiscordException as e:
            print(f"Error sending embed: {e}")

    @command(name="help", description="Shows help for the bot")
    @describe(modules="Modules to choose from")
    @choices(
        modules=[
            Choice(name="Memo", value="memo"),
            Choice(name="TicTacToe", value="tic_tac_toe"),
            Choice(name="FlagGuesser", value="flag_guesser"),
            Choice(name="Miscellaneous", value="miscellaneous"),
            Choice(name="Reddit", value="reddit"),
            Choice(name="All", value="all"),
        ],
    )
    async def help(
        self,
        interaction: discord.Interaction,
        modules: Choice[str],
    ) -> None:
        """Handle the help command based on the chosen module.

        Args:
            interaction (discord.Interaction): The interaction
            module: The chosen help module, provided as an option.

        Depending on the chosen module, calls the appropriate help function.
        """
        # Based on the chosen module, call the appropriate help function
        module = modules.value
        if module == "memo":
            await self.memo_help(interaction)
        elif module == "tic_tac_toe":
            await self.tic_tac_toe_help(interaction)
        elif module == "flag_guesser":
            await self.flag_guesser_help(interaction)
        elif module == "miscellaneous":
            await self.mini_commands_help(interaction)
        elif module == "reddit":
            await self.reddit_help(interaction)
        elif module == "all":
            await self.all_help(interaction)


async def setup(client: discord.ext.commands.Bot) -> None:
    """Adds the Help cog to the bot

    Args:
        client (discord.ext.commands.Bot): The client object
    """
    await client.add_cog(Help(client))
