"""This module contains the EmbedBuilder class."""

import discord
from typing import List, Dict, Any


class EmbedBuilder:
    """A class to build discord embeds."""

    def __init__(
        self, title: str = None, description: str = None, color: tuple = (255, 255, 255)
    ):
        self.embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.from_rgb(*[min(max(c, 0), 255) for c in color]),
        )
        self.embed.set_footer(
            text="『Xrbot』",
            icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU",
        )

    def add_field(self, name: str, value: str, inline: bool = False) -> None:
        """Add a field to the embed.

        Args:
            name (str): name of the field
            value (str): value of the field
            inline (bool, optional): whether the field should be inline. Defaults to False.
        """
        self.embed.add_field(name=name, value=value, inline=inline)

    def add_bulk_fields(self, fields: List[Dict[str, Any]]) -> None:
        """Add bulk fields to the embed

        Args:
            fields:
        """
        for field in fields:
            self.add_field(field["name"], field["value"], field.get("inline", False))

    def set_footer(self, text: str, icon_url: str = None) -> None:
        """Set the footer of the embed.

        Args:
            text (str): text of the footer
            icon_url (str, optional): url of the icon. Defaults to None.
        """
        self.embed.set_footer(text=text, icon_url=icon_url)

    def set_image(self, url: str) -> None:
        """Set the image of the embed.

        Args:
            url (str): url of the image
        """
        self.embed.set_image(url=url)

    def set_thumbnail(self, url: str) -> None:
        """Set the thumbnail of the embed.

        Args:
            url (str): url of the thumbnail
        """
        self.embed.set_thumbnail(url=url)

    def set_author(self, name: str, icon_url: str = None) -> None:
        """Set the author of the embed.

        Args:
            name (str): name of the author
            icon_url (str, optional): url of the icon. Defaults to None.
        """
        self.embed.set_author(name=name, icon_url=icon_url)

    def build(self) -> discord.Embed:
        """Get the embed.

        Returns:
            _type_: discord.Embed: the embed
        """
        return self.embed
