import discord
import os
from cogs.MiniCommands import MiniCommands
from cogs.MemoCommands import MemoCommands
from cogs.TicTacToe import TicTacToe
from cogs.FlagGuesser import FlagGuesser
from cogs.HelpCommands import HelpCommands
from cogs.RedditCommands import RedditCommands
from cogs.WebScrapingCommands import WebScrapingCommands
from MusicCommands import MusicCommands
from KeepAlive import keep_alive
from discord.ext import commands



class Bot(commands.Bot):
  def __init__(self):
    intents=discord.Intents.default()
    intents.message_content = True
    super().__init__(command_prefix="x!", case_insensitive=True, intents=intents)

  async def setup_hook(self):
    self.remove_command('help')
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        await self.load_extension(f"cogs.{filename[:-3]}")
        
    await self.tree.sync(guild = discord.Object(id="1033487447885103244"))
    print(f"Synced slash commands for {self.user}")

  async def on_command_error(self, ctx, error):
    await ctx.reply(error, ephemeral = True)
  
  async def on_ready(self):
    print(f"We have logged in as {self.user}")
    
    # Setting `Watching ` status
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Learn Hebrew while sleeping 8h version"))
  
Bot = Bot()

@Bot.hybrid_command(name= "test", with_app_command = True, description="test command")
async def test(ctx: commands.Context):
  await ctx.defer(ephemeral = True)
  await ctx.send("hi")
  
class autoresponse(commands.Cog):
    def __init__(self, Bot):
        self.bot = Bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if(str(message.author)=="『Xrgon』#7135"):            
          emoji = discord.utils.get(message.guild.emojis, name="nerdbob")
          await message.add_reaction(emoji)
  
#
      
my_secret = os.environ["BotToken"]
keep_alive()
Bot.run(my_secret)