"""Module for web scraping commands"""

from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup
import discord
from discord import Interaction
from discord.ext import commands
from discord.app_commands import command, describe, CommandTree
import pandas as pd
from core.embed_builder import EmbedBuilder
from core.util import Util


class WebScrapingCommands(commands.Cog, name="get"):
    """Class for WebScraping commands

    Args:
        commands (commands.Cog): The commands object
    """

    def __init__(self, bot):
        self.bot = bot
        self.logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU"

    @command(name="lyrics", description="Gets the lyrics of a song")
    @describe(song="The song name")
    async def get_lyrics(self, interaction: Interaction, song: str) -> None:
        """Gets the lyrics of a song

        Args:
            interaction (Interaction): The interaction object
            song (str): The song name
        """
        url = f"https://genius.com/{song}-lyrics"
        req = Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )  # Opens genius page of song

        try:
            webpage = urlopen(req).read()  # Checks if page exists
        except:
            await interaction.response.send_message("Song or Aritst name is wrong")
            return

        soup = BeautifulSoup(webpage, "lxml")

        # Get title of song
        regex = re.compile(".*SongHeaderdesktop.*")
        title = soup.find("h1", attrs={"class": regex}).text.strip()
        album = soup.find("a", attrs={"href": "#primary-album"}).text.strip()

        links = []
        for i in range(5):
            for link in soup.findAll("a"):
                links.append(link.get("href"))

        artist = soup.find("a", attrs={"href": links[5]}).text.strip()

        embed_builder = EmbedBuilder(
            title=title,
            description=f"by {artist} on {album}",
            color=(0, 0, 0),
        )

        # get Lyrics
        regex = re.compile(".*Lyrics__Container.*")
        lyrics = soup.find("div", attrs={"class": regex}).text.strip()

        lyrics = Util.format_lyrics(lyrics)

        split_lyrics = Util.split_lyrics(lyrics)

        # Formatting done now add to embed
        for i, part in enumerate(split_lyrics):
            embed_builder.add_field(
                name=f"Lyrics Part {i + 1}:", value=part, inline=False
            )

        # Get song image
        images = []
        for img in soup.findAll("img"):
            images.append(img.get("src"))

        embed_builder.set_thumbnail(url=images[1])

        embed_builder.add_field(
            name="Links:", value=f"Artist: {links[5]}\nSong: URL", inline=False
        )

        embed_builder.set_footer(
            text="Lyrics from https://genius.com/", icon_url=self.logo
        )
        await interaction.response.send_message(embed=embed_builder)

    @command(name="weather", description="Gets the weather of a city")
    @describe(city="The city name", country="The country name")
    async def get_weather(
        self, interaction: Interaction, city: str, country: str
    ) -> None:
        """Gets the weather of a city

        Args:
            interaction (Interaction): The interaction object
            city (str): The city name
            country (str): The country name
        """
        url = f"https://www.timeanddate.com/weather/{country}/{city}/hourly"

        try:
            forecast = pd.read_html(url)  # Checks if page exists

        except:
            await ctx.send(
                "Country or City name is wrong/nx!get weather [country] [city]"
            )
            return

        table = forecast[1]
        weather_times = table.iloc[0, 0:5]
        weather_temp = table.iloc[2, 0:5]

        weather = ""
        for i in range(5):  # Gets weather for the next 5 hours
            weather += f"{weather_times[i]}----> "
            weather += (
                str(
                    round(
                        (float(re.search(r"\d+", weather_temp[i]).group()) - 32)
                        * (5 / 9)
                    )
                )
                + " °C"
            )
            weather += "\n-------------------------------\n"

        embed_builder = EmbedBuilder(
            title="Weather in " + city + ", " + country,
            description=weather,
            color=(0, 0, 0),
        )

        embed_builder.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfnS75QwwkgQCc01HRB3SQOQDrAbqCW4D_3g&usqp=CAU"
        )

        embed_builder.set_footer(text=f"weather from {url}", icon_url=self.logo)

        await interaction.response.send_message(embed=embed_builder.build())


async def setup(client: discord.ext.commands.Bot) -> None:
    """Adds the WebScrapingCommands cog to the bot

    Args:
        client (discord.ext.commands.Bot): The client object
    """
    await client.add_cog(WebScrapingCommands(client))
