#Functions of the commands related to the FlagGuesser features of the bot
import discord
from discord.ext import commands
import HelpCommands
import random

  
class FlagGuesser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.Answer = ""  # Correct answer
        self.Choice = 0  # Correct Choice
        self.GameOngoing = False  # State of game
        self.Turn = 1  # Turn 
        self.Score = 0  # Number of correct guesses
        self.Countries = [] # Countries and Country codes

      
    @commands.command(name="FlagGuesser", aliases=["fg"])
    async def Aliases(self, ctx):
        if ((ctx.message.content).lower().startswith("x!flagguesser start")
        or (ctx.message.content).lower().startswith("x!fg start")):
           await FlagGuesser.FlagGuesserStart(self, ctx)
        elif ((ctx.message.content).lower().startswith("x!flagguesser end")
        or (ctx.message.content).lower().startswith("x!fg end")):
           await FlagGuesser.FlagGuesserEnd(self,ctx)
        elif ((ctx.message.content).lower().startswith("x!flagguesser guess ")      
        or (ctx.message.content).lower().startswith("x!fg guess ")):
           await FlagGuesser.FlagGuesserGuess(self, ctx)
        else:
           await HelpCommands.FlagGuesserHelp(ctx)


    async def FlagGuesserEnd(self, ctx):  # To end current game
        if (self.GameOngoing):
            await ctx.send("FlagGuesser game ended")
            self.GameOngoing = False
            FlagGuesser.GameReset(self)
        else:
          await ctx.send("No ongoing FlagGuesser game")

                
    async def FlagGuesserSend(self, ctx):  # To send the next flag 
        Country = self.Countries.pop(random.randint(0,len(self.Countries)-1))  # Gets random country
        CountryCode = Country[0].lower()  # Saves country code
        self.Answer = Country[1]  # Save correct country name
        URL = f"https://flagpedia.net/data/flags/w580/{CountryCode}.png"
      
        Embed = discord.Embed(title=f"Flag #{str(self.Turn)}",
                              color=discord.Color.from_rgb(20, 255, 0))
                              
        Embed.set_image(url=URL)
        await ctx.send(embed=Embed)

        RandomCountry_1 = self.Countries[random.randint(0,len(self.Countries))][1]  # Random choice 1
        RandomCountry_2 = self.Countries[random.randint(0,len(self.Countries))][1]  # Random choice 2
      
        while(RandomCountry_1 == RandomCountry_2):  # Making sure Random choice 1 != Random choice 2
            RandomCountry_2 = self.Countries[random.randint(0,len(self.Countries))][1]
        
        Choices = [self.Answer,RandomCountry_1,RandomCountry_2]  # Randomize the choices
        Result = "Pick the correct country: x!flagguesser guess [#] or x!fg guess [#]"
      
        for i in range(3):
            Random = random.randint(0,len(Choices)-1)
            Result += f"\n{str(i+1)}- {Choices[Random]}"
            if(Choices[Random] == self.Answer):
                self.Choice = i+1  # Correct choice
            Choices.pop(Random)
        await ctx.send(Result)

  
    async def FlagGuesserGuess(self, ctx):  # Checks if user guess is correct
        if(not self.GameOngoing):
            await ctx.send("No ongoing FlagGuesser game")
            return
        if (ctx.message.content.lower().startswith("x!flagguesser guess ")):
          UserGuess = ctx.message.content.lower().replace("x!flagguesser guess ","")
        elif(ctx.message.content.lower().startswith("x!fg guess ")):
          UserGuess = ctx.message.content.lower().replace("x!fg guess ","")
          
        try:  # Checks input is integer and not string
            UserGuess = int(UserGuess)
        except:
            await ctx.send("Incorrect format\nx!flagguesser guess [Guess number] | x!fg guess [Guess number]")
            return
          
        if(UserGuess>3):
            await ctx.send("Incorrect format\nx!flagguesser guess [Guess number] | x!fg guess [Guess number]")
          
        if (UserGuess == self.Choice):
            await ctx.send("Correct guess, +1 points")
            self.Score += 1
        else:
            await ctx.send(f"Wrong guess :(\nCorrect guess was {self.Answer}")
        self.Turn += 1
        
        if(self.Turn == 11):  # If game has reached turn == 11 then it ends
            await ctx.send(f"Your final score is {str(self.Score)}/10!")
            self.GameOngoing = False
            FlagGuesser.GameReset(self)
        else:
            await FlagGuesser.FlagGuesserSend(self, ctx)
  
    async def FlagGuesserStart(self, ctx):  # Starts game
        if (self.GameOngoing):
            await ctx.send(
              "Current Flag Guesser ongoing \nx!FlagGuesser end | x!fg end if you wish to end it")
        else:
            FlagGuesser.GameReset(self)
            self.GameOngoing = True
            await ctx.send(
              "Guess country name of the following 10 flags\nx!FlagGuesser end | x!fg end if you wish to end it")
            await FlagGuesser.FlagGuesserSend(self, ctx)

    def GameReset(self):  # Resets game 
        self.Turn = 1  # What turn the game is on
        self.Score = 0  # Number of correct guesses
        self.Choice = 0  # Correct Choice
        self.Countries = [
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
        ("ZW", "Zimbabwe")]  # Countries and Country codes

