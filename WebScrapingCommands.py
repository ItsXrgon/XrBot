from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import discord
import pandas as pd
from discord.ext import commands
import HelpCommands


class WebScrapingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU"
  
    @commands.command(name="get")
    async def Aliases(self, ctx):
        if(ctx.message.content).lower().startswith("x!get weather "):
            await WebScrapingCommands.GetWeather(self, ctx)
        elif(ctx.message.content).lower().startswith("x!get lyrics "):
            await WebScrapingCommands.GetLyrics(self, ctx)        
        else:
            await HelpCommands.GetHelp(ctx) 

    
    async def GetLyrics(self, ctx):  # Gets lyrics of song   
        Input = ctx.message.content.lower().replace("x!get lyrics ","").replace(" ", "-")
    
        URL = f"https://genius.com/{Input}-lyrics"
        Req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})  # Opens genius page of song
    
        try:
            Webpage = urlopen(Req).read()  # Checks if page exists
    
        except:
            await ctx.send("Song or Aritst name is wrong")
            return
    
        soup = BeautifulSoup(Webpage, "lxml")  
    
        # Get title of song
        Regex = re.compile(".*SongHeaderdesktop.*")
        TitleBox = soup.find("h1", attrs={"class": Regex})
        Title = TitleBox.text.strip()
    
        # Get Album name
        AlbumBox = soup.find("a", attrs={"href": "#primary-album"})  # get title
        Album = AlbumBox.text.strip()
    
        # Get artist name and link
        Links = []
        for i in range(5):
            for link in soup.findAll("a"):
                Links.append(link.get("href"))
    
        ArtistBox = soup.find("a", attrs={"href": Links[5]})
        Artist = ArtistBox.text.strip()
    
        Embed = discord.Embed(title=Title,
                              description=f"by {Artist} on {Album}",
                              color=discord.Color.from_rgb(0, 0, 0))
    
        # get Lyrics
        Regex = re.compile(".*Lyrics__Container.*")
        LyricsBox = soup.find("div", attrs={"class": Regex})
        UnformattedLyrics = LyricsBox.text.strip()
    
        # Formatting the lyrics to look better
        Lyrics = ""
        for i in range(len(UnformattedLyrics) - 2):
            Lyrics += UnformattedLyrics[i]
            if ((UnformattedLyrics[i].islower() and UnformattedLyrics[i + 1].isupper()) 
                
            or ((UnformattedLyrics[i] == "?" or UnformattedLyrics[i] == "!" or UnformattedLyrics[i] == ")")
            and UnformattedLyrics[i + 1] != "[" and UnformattedLyrics[i + 1] != "'"
            and UnformattedLyrics[i + 1] != ")")
                
            or (UnformattedLyrics[i].isupper()
            and UnformattedLyrics[i + 1].isupper()
            and UnformattedLyrics[i + 2].islower())
               
            or (UnformattedLyrics[i] == "'" and UnformattedLyrics[i + 1] == "'")
            or (UnformattedLyrics[i] == ")" and UnformattedLyrics[i + 1] == "'")
            or (UnformattedLyrics[i] == ".")
            or (UnformattedLyrics[i] == ";")):
                Lyrics += "\n"
    
        Lyrics += UnformattedLyrics[len(UnformattedLyrics) - 1]
        Lyrics += UnformattedLyrics[len(UnformattedLyrics) - 2]
    
        Lyrics = Lyrics.split("[")
        Lyrics = "\n\n[".join(Lyrics)
    
        Lyrics = Lyrics.split("]")
        Lyrics = "]\n".join(Lyrics)

        Lyrics1 = None
        Lyrics2 = None
        Lyrics3 = None  
    
        # Splitting lyrics into 3 parts depending on its size
        if (len(Lyrics) > 1024):
            for i in range(1024, 0, -1):
                if (Lyrics[i] == "\n"):
                    break
    
            Lyrics1 = Lyrics[0:i]
            Lyrics2 = Lyrics[i:len(Lyrics)]
    
            if (len(Lyrics2) > 1024):
                for i in range(1024, 0, -1):
                    if (Lyrics2[i] == "\n"):
                        break
    
                Lyrics = Lyrics2
                Lyrics2 = Lyrics[0:i]
                Lyrics3 = Lyrics[i:len(Lyrics)]
    
        # Formatting done now add to embed
        if (Lyrics1 != None):
            Embed.add_field(name="Lyrics:", value=Lyrics1, inline=False)
        else:
            Embed.add_field(name="Lyrics:", value=Lyrics, inline=False)
          
        if (Lyrics2 != None):
            Embed.add_field(name="Lyrics:", value=Lyrics2, inline=False)
    
        if (Lyrics3 != None):
            Embed.add_field(name="Lyrics:", value=Lyrics3, inline=False)
    
        # Get songs image
        Images = []
        for img in soup.findAll("img"):
            Images.append(img.get("src"))
    
        Embed.set_thumbnail(url=Images[1])
    
        Embed.add_field(name="Links:",
                        value=f"Artist: {Links[5]}\nSong: URL",
                        inline=False)
    
        Embed.set_footer(
            text="Lyrics from https://genius.com/",
            icon_url=self.Logo)
        await ctx.send(embed=Embed)
    
    
    async def GetWeather(self, ctx):  # Gets weather of city
    
        Input = ctx.message.content.lower().replace("x!get weather ", "").replace(" ", "/")
        URL = f"https://www.timeanddate.com/weather/{Input}"
    
        try:
            Forecast = pd.read_html(URL)   # Checks if page exists
    
        except:
            await ctx.send(
                "Country or City name is wrong/nx!get weather [country] [city]")
            return
    
        Table = Forecast[1]
        WeatherTimes = Table.iloc[0, 0:5]
        WeatherTemp = Table.iloc[2, 0:5]
    
        Weather = ""
        for i in range(5):  # Gets weather for the next 5 hours
    
            Weather += f"{WeatherTimes[i]}----> "
            Weather += str(
                round((float(re.search(r"\d+", WeatherTemp[i]).group()) - 32) *
                      (5 / 9))) + " °C"
            Weather += "\n-------------------------------\n"
    
        Embed = discord.Embed(title="Weather in " + Input.replace("/", ", "),
                              description=Weather,
                              color=discord.Color.from_rgb(0, 0, 0))
    
        Embed.set_thumbnail(
        url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfnS75QwwkgQCc01HRB3SQOQDrAbqCW4D_3g&usqp=CAU")
    
        Embed.set_footer(
            text=f"weather from {URL}",
            icon_url=self.Logo)
      
        await ctx.send(embed=Embed)
