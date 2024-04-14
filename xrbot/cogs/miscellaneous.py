"""Functions of the commands related to the Miscellaneous features of the bot"""

import os
import random
import discord
from discord import Interaction
from discord.app_commands import command, describe, checks, commands, CommandTree


class MiscellaneousCommands(commands.Group, name="misc"):
    """Class for Miscellaneous commands

    Args:
        commands (commands.Cog): The commands object
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @command(
        name="number-between", description="Chooses a random number between two inputs"
    )
    @describe(num1="The first number", num2="The second number")
    async def number_between(
        self, interaction: Interaction, num1: int, num2: int
    ) -> None:
        """Chooses a random number between two inputs.

        Args:
            interaction (Interaction): The interaction object.
            num1 (int): The first input number.
            num2 (int): The second input number.
        """
        lower_bound = min(num1, num2)
        upper_bound = max(num1, num2)

        random_number = random.randint(lower_bound, upper_bound)

        result = (
            f"Random number between {lower_bound} and {upper_bound} is {random_number}."
        )

        # Send the response
        await interaction.response.send_message(result)

    @command(
        name="coinflip",
        description="Flips a coin and returns heads or tails",
    )
    async def coin_flip(self, interaction: Interaction) -> None:
        """Flips a coin and returns heads or tails

        Args:
            interaction (Interaction): The interaction object
        """
        result = "Heads" if (random.randint(0, 1) == 1) else "Tails"
        await interaction.response.send_message(result)

    # @command(
    #     name="spin-the-bottle",
    #     description="Spins a bottle and gives who its pointing to & from",
    # )
    # @describe(
    #     participants="The participants of the game",
    # )
    # async def spin_the_bottle(
    #     self,
    #     interaction: Interaction,
    #     participants: commands.Greedy[discord.User],
    # ):
    #     """Spins a bottle and gives who its pointing to & from"

    #     Args:
    #         interaction (Interaction): The interaction object
    #         participants (commands.Greedy[discord.User]): The participants of the game
    #     """
    #     bottle_front = participants[random.randint(0, len(participants) - 1)]
    #     bottle_back = participants[random.randint(0, len(participants) - 1)]

    #     # incase front and back point at same participant
    #     while bottle_front == bottle_back:
    #         bottle_back = participants[random.randint(0, len(participants) - 1)]

    #     result = f"bottle has been spun and is now pointing at {bottle_front} from {bottle_back}"
    #     await interaction.response.send_message(result)

    @command(
        name="move-messages",
        description="Move the indicated number of messages to the indicated channel",
    )
    @describe(
        message_count="Number of messages to move",
        destination_channel="Channel to move messages to",
    )
    @checks.has_permissions(manage_messages=True)
    async def move_chat(
        self,
        interaction: Interaction,
        message_count: int,
        destination_channel: str,
    ) -> None:
        """Move the indicated number of messages to the indicated channel

        Args:
            interaction (Interaction): The interaction object
            message_count (int): The number of messages to move
            destination_channel (str): The channel to move to
        """

        messages = await interaction.channel.history(
            limit=int(message_count) + 1
        ).flatten()

        i = len(messages) - 1
        while i > 0:
            message = messages[i]
            i -= 1
        await destination_channel.send(f"{message.author.name}: {message.content}")
        j = 0
        while j < len(message.attachments):
            await destination_channel.send(message.attachments[j].url)
            j += 1
        await interaction.channel.purge(limit=int(len(messages)) + 1)

    @command(
        name="purge-messages",
        description="Purges the indicated number of messages",
    )
    @describe(
        message_count="Number of messages to purge",
    )
    @checks.has_permissions(manage_messages=True)
    async def purge(
        self,
        interaction: Interaction,
        message_count: int,
    ) -> None:
        """Purges the indicated number of messages

        Args:
            interaction (Interaction): The interaction object
            message_count (int): he number of messages to purge
        """
        await interaction.channel.purge(limit=int(message_count) + 1)

    @command(
        name="pengu-roll",
        description="Display an image of a random penguin",
    )
    async def pengu_roll(self, interaction: Interaction) -> None:
        """Display an image of a random penguin

        Args:
            interaction (Interaction): The interaction object
        """
        path = random.choice(os.listdir("assets/penguin_images/"))
        pengu = discord.File("assets/penguin_images/" + path)
        pengu_name = "***" + path.replace(".png", "") + "***"
        await interaction.response.send_message(pengu_name, file=pengu)


async def setup(client: discord.Client) -> None:
    """Adds the MiscellaneousCommands cog to the bot

    Args:
        client (discord.Client): The client object
    """
    await client.add_cog(MiscellaneousCommands(client))
