# Functions of the commands related to the FlagGuesser features of the bot
import discord
from discord import Interaction
from discord.ext import commands
from discord.app_commands import command, describe
from core.embed_builder import EmbedBuilder
import random


class FlagGuesser(commands.Cog, name="flag-guesser"):
    """Class for FlagGuesser commands

    Args:
        commands (commands.Group): The commands object
    """

    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @command(name="end", description="Ends the FlagGuesser game")
    async def end(self, interaction: Interaction):
        """Ends the FlagGuesser game

        Args:
            interaction (Interaction): The interaction object
        """
        try:
            self.games[interaction.channel.id]
        except:
            await interaction.response.send_message("No ongoing FlagGuesser game")
        else:
            await interaction.channel.send("FlagGuesser game ended")
            del self.games[interaction.channel.id]

    async def send_flag(self, interaction: Interaction):
        """Sends the flag to the channel

        Args:
            interaction (Interaction): The interaction object
        """
        game = self.games.get(interaction.channel.id)

        country_index = random.randint(0, len(game.Countries) - 1)
        country = game.Countries.pop(country_index)
        country_code = country[0].lower()
        game.Answer = country[1]
        flag_url = f"https://flagpedia.net/data/flags/w580/{country_code}.png"

        embed_builder = EmbedBuilder(
            title=f"Flag #{str(self.games[interaction.channel.id].Turn)}",
            color=discord.Color.from_rgb(20, 255, 0),
        )

        embed_builder.set_image(url=flag_url)
        await interaction.channel.send(embed=embed_builder.build())

        remaining_countries = [c[1] for c in game.Countries]
        if game.answer in remaining_countries:
            remaining_countries.remove(game.answer)

        choices = [game.answer]
        choices.extend(random.sample(remaining_countries, 2))

        # Shuffle the choices for presentation
        random.shuffle(choices)

        # Store the correct choice for future reference
        game.choice = choices.index(game.answer) + 1

        result = "Pick the correct country: /FlagGuesser Guess <number>\n"
        for idx, choice in enumerate(choices, start=1):
            result += f"{idx}- {choice}\n"

        await interaction.channel.send(result)

    @command(name="guess", description="Take a guess in flag guesser game")
    @describe(guess="The guess number")
    async def take_guess(self, interaction: Interaction, guess: int):
        """Take a guess in flag guesser game

        Args:
            interaction (Interaction): The interaction object
            guess (int): The guess number
        """
        if self.games[interaction.channel.id] == None:
            await interaction.response.send_message("No ongoing FlagGuesser game")
            return

        if guess > 3:
            await interaction.response.send_message(
                "Incorrect format\nx!flagguesser guess [Guess number] | x!fg guess [Guess number]"
            )

        if guess == self.games[interaction.channel.id].choice:
            await interaction.channel.send("Correct guess, +1 points")
            self.games[interaction.channel.id].Score += 1
        else:
            await interaction.channel.send(
                f"Wrong guess :(\nCorrect guess was {self.games[interaction.channel.id].Answer}"
            )

        if self.games[interaction.channel.id].Turn == 10:
            await interaction.channel.send(
                f"Your final score is {str(self.games[interaction.channel.id].Score)}/10!"
            )
            del self.games[interaction.channel.id]
        else:
            self.games[interaction.channel.id].Turn += 1
            await FlagGuesser.send_flag(self, interaction)

    @command(name="start", description="Starts the FlagGuesser game")
    async def start_game(self, interaction: Interaction):
        """Starts the FlagGuesser game

        Args:
            interaction (Interaction): The interaction object
        """
        try:
            self.games[interaction.channel.id]
        except:
            self.games[interaction.channel.id] = FlagGuesserGame()
            await interaction.response.send_message(
                "Guess country name of the following 10 flags\nx!FlagGuesser end | x!fg end if you wish to end it"
            )
            await FlagGuesser.send_flag(self, interaction)
        else:
            await interaction.response.send_message.send(
                "Current Flag Guesser ongoing, end it before starting a new one"
            )


class FlagGuesserGame:
    """Class to store the game data for FlagGuesser"""

    def __init__(self):
        self.answer = ""  # Correct answer
        self.turn = 1  # What turn the game is on
        self.score = 0  # Number of correct guesses
        self.choice = 0  # Correct Choice
        self.countries = [
            ("US", "United States"),
            ("AF", "Afghanistan"),
            ("AL", "Albania"),
            ("DZ", "Algeria"),
            ("AS", "American Samoa"),
            ("AD", "Andorra"),
            ("AO", "Angola"),
            ("AI", "Anguilla"),
            ("AQ", "Antarctica"),
            ("AG", "Antigua And Barbuda"),
            ("AR", "Argentina"),
            ("AM", "Armenia"),
            ("AW", "Aruba"),
            ("AU", "Australia"),
            ("AT", "Austria"),
            ("AZ", "Azerbaijan"),
            ("BS", "Bahamas"),
            ("BH", "Bahrain"),
            ("BD", "Bangladesh"),
            ("BB", "Barbados"),
            ("BY", "Belarus"),
            ("BE", "Belgium"),
            ("BZ", "Belize"),
            ("BJ", "Benin"),
            ("BM", "Bermuda"),
            ("BT", "Bhutan"),
            ("BO", "Bolivia"),
            ("BA", "Bosnia And Herzegowina"),
            ("BW", "Botswana"),
            ("BV", "Bouvet Island"),
            ("BR", "Brazil"),
            ("BN", "Brunei Darussalam"),
            ("BG", "Bulgaria"),
            ("BF", "Burkina Faso"),
            ("BI", "Burundi"),
            ("KH", "Cambodia"),
            ("CM", "Cameroon"),
            ("CA", "Canada"),
            ("CV", "Cape Verde"),
            ("KY", "Cayman Islands"),
            ("CF", "Central African Rep"),
            ("TD", "Chad"),
            ("CL", "Chile"),
            ("CN", "China"),
            ("CX", "Christmas Island"),
            ("CC", "Cocos Islands"),
            ("CO", "Colombia"),
            ("KM", "Comoros"),
            ("CG", "Congo"),
            ("CK", "Cook Islands"),
            ("CR", "Costa Rica"),
            ("CI", "Cote D`ivoire"),
            ("HR", "Croatia"),
            ("CU", "Cuba"),
            ("CY", "Cyprus"),
            ("CZ", "Czech Republic"),
            ("DK", "Denmark"),
            ("DJ", "Djibouti"),
            ("DM", "Dominica"),
            ("DO", "Dominican Republic"),
            ("TP", "East Timor"),
            ("EC", "Ecuador"),
            ("EG", "Egypt"),
            ("SV", "El Salvador"),
            ("GQ", "Equatorial Guinea"),
            ("ER", "Eritrea"),
            ("EE", "Estonia"),
            ("ET", "Ethiopia"),
            ("FK", "Falkland Islands (Malvinas)"),
            ("FO", "Faroe Islands"),
            ("FJ", "Fiji"),
            ("FI", "Finland"),
            ("FR", "France"),
            ("GF", "French Guiana"),
            ("PF", "French Polynesia"),
            ("TF", "French S. Territories"),
            ("GA", "Gabon"),
            ("GM", "Gambia"),
            ("GE", "Georgia"),
            ("DE", "Germany"),
            ("GH", "Ghana"),
            ("GI", "Gibraltar"),
            ("GR", "Greece"),
            ("GL", "Greenland"),
            ("GD", "Grenada"),
            ("GP", "Guadeloupe"),
            ("GU", "Guam"),
            ("GT", "Guatemala"),
            ("GN", "Guinea"),
            ("GW", "Guinea-bissau"),
            ("GY", "Guyana"),
            ("HT", "Haiti"),
            ("HN", "Honduras"),
            ("HK", "Hong Kong"),
            ("HU", "Hungary"),
            ("IS", "Iceland"),
            ("IN", "India"),
            ("ID", "Indonesia"),
            ("IR", "Iran"),
            ("IQ", "Iraq"),
            ("IE", "Ireland"),
            ("IL", "Israel"),
            ("IT", "Italy"),
            ("JM", "Jamaica"),
            ("JP", "Japan"),
            ("JO", "Jordan"),
            ("KZ", "Kazakhstan"),
            ("KE", "Kenya"),
            ("KI", "Kiribati"),
            ("KP", "Korea (North)"),
            ("KR", "Korea (South)"),
            ("KW", "Kuwait"),
            ("KG", "Kyrgyzstan"),
            ("LA", "Laos"),
            ("LV", "Latvia"),
            ("LB", "Lebanon"),
            ("LS", "Lesotho"),
            ("LR", "Liberia"),
            ("LY", "Libya"),
            ("LI", "Liechtenstein"),
            ("LT", "Lithuania"),
            ("LU", "Luxembourg"),
            ("MO", "Macau"),
            ("MK", "Macedonia"),
            ("MG", "Madagascar"),
            ("MW", "Malawi"),
            ("MY", "Malaysia"),
            ("MV", "Maldives"),
            ("ML", "Mali"),
            ("MT", "Malta"),
            ("MH", "Marshall Islands"),
            ("MQ", "Martinique"),
            ("MR", "Mauritania"),
            ("MU", "Mauritius"),
            ("YT", "Mayotte"),
            ("MX", "Mexico"),
            ("FM", "Micronesia"),
            ("MD", "Moldova"),
            ("MC", "Monaco"),
            ("MN", "Mongolia"),
            ("MS", "Montserrat"),
            ("MA", "Morocco"),
            ("MZ", "Mozambique"),
            ("MM", "Myanmar"),
            ("NA", "Namibia"),
            ("NR", "Nauru"),
            ("NP", "Nepal"),
            ("NL", "Netherlands"),
            ("AN", "Netherlands Antilles"),
            ("NC", "New Caledonia"),
            ("NZ", "New Zealand"),
            ("NI", "Nicaragua"),
            ("NE", "Niger"),
            ("NG", "Nigeria"),
            ("NU", "Niue"),
            ("NF", "Norfolk Island"),
            ("MP", "Northern Mariana Islands"),
            ("NO", "Norway"),
            ("OM", "Oman"),
            ("PK", "Pakistan"),
            ("PW", "Palau"),
            ("PA", "Panama"),
            ("PG", "Papua New Guinea"),
            ("PY", "Paraguay"),
            ("PE", "Peru"),
            ("PH", "Philippines"),
            ("PN", "Pitcairn"),
            ("PL", "Poland"),
            ("PT", "Portugal"),
            ("PR", "Puerto Rico"),
            ("QA", "Qatar"),
            ("RE", "Reunion"),
            ("RO", "Romania"),
            ("RU", "Russian Federation"),
            ("RW", "Rwanda"),
            ("KN", "Saint Kitts And Nevis"),
            ("LC", "Saint Lucia"),
            ("VC", "St Vincent/Grenadines"),
            ("WS", "Samoa"),
            ("SM", "San Marino"),
            ("ST", "Sao Tome"),
            ("SA", "Saudi Arabia"),
            ("SN", "Senegal"),
            ("SC", "Seychelles"),
            ("SL", "Sierra Leone"),
            ("SG", "Singapore"),
            ("SK", "Slovakia"),
            ("SI", "Slovenia"),
            ("SB", "Solomon Islands"),
            ("SO", "Somalia"),
            ("ZA", "South Africa"),
            ("ES", "Spain"),
            ("LK", "Sri Lanka"),
            ("SH", "St. Helena"),
            ("PM", "St.Pierre"),
            ("SD", "Sudan"),
            ("SR", "Suriname"),
            ("SZ", "Swaziland"),
            ("SE", "Sweden"),
            ("CH", "Switzerland"),
            ("SY", "Syrian Arab Republic"),
            ("TW", "Taiwan"),
            ("TJ", "Tajikistan"),
            ("TZ", "Tanzania"),
            ("TH", "Thailand"),
            ("TG", "Togo"),
            ("TK", "Tokelau"),
            ("TO", "Tonga"),
            ("TT", "Trinidad And Tobago"),
            ("TN", "Tunisia"),
            ("TR", "Turkey"),
            ("TM", "Turkmenistan"),
            ("TV", "Tuvalu"),
            ("UG", "Uganda"),
            ("UA", "Ukraine"),
            ("AE", "United Arab Emirates"),
            ("UK", "United Kingdom"),
            ("UY", "Uruguay"),
            ("UZ", "Uzbekistan"),
            ("VU", "Vanuatu"),
            ("VA", "Vatican City State"),
            ("VE", "Venezuela"),
            ("VN", "Viet Nam"),
            ("VG", "Virgin Islands (British)"),
            ("VI", "Virgin Islands (U.S.)"),
            ("YE", "Yemen"),
            ("YU", "Yugoslavia"),
            ("ZR", "Zaire"),
            ("ZM", "Zambia"),
            ("ZW", "Zimbabwe"),
        ]


async def setup(client: discord.ext.commands.Bot) -> None:
    """Adds the FlagGuesser cog to the bot

    Args:
        client (discord.ext.commands.Bot): The client object
    """
    await client.add_cog(FlagGuesser(client))
