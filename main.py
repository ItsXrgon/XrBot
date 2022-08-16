import discord
import os
from MiniCommands import MiniCommands
from MemoCommands import MemoCommands
from TicTacToe import TicTacToe
from FlagGuesser import FlagGuesser
from HelpCommands import HelpCommands
from RedditCommands import RedditCommands
from WebScrapingCommands import WebScrapingCommands
from MusicCommands import MusicCommands
from KeepAlive import keep_alive
from discord.ext import commands


Bot = commands.Bot(command_prefix="x!", case_insensitive=True)

@Bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(Bot))
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Learn Hebrew while sleeping 8h version"))
    # Setting `Playing ` status
    #await client.change_presence(activity=discord.Game(name="pain"))
    
    # Setting `Watching ` status
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the errors"))

Bot.remove_command('help')
Bot.add_cog(MiniCommands(Bot))
Bot.add_cog(MemoCommands(Bot))
Bot.add_cog(WebScrapingCommands(Bot))
Bot.add_cog(MusicCommands(Bot))
Bot.add_cog(FlagGuesser(Bot))
Bot.add_cog(RedditCommands(Bot))
Bot.add_cog(TicTacToe(Bot))
Bot.add_cog(HelpCommands(Bot))


my_secret = os.environ["BotToken"]
keep_alive()
Bot.run(my_secret)