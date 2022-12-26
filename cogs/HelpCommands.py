#Functions of the commands related to the Help features of the bot
import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    async def setup(bot: commands.Bot) -> None:
      await bot.add_cog(
        HelpCommands(bot),
        guilds = [discord.Object(id="1033487447885103244")]
      )
  
    @commands.command(name="help")
    async def Aliases(self, ctx):
        if (ctx.message.content).lower().startswith("x!help"):
            if (ctx.message.content).lower().startswith("x!help memo"):
               await HelpCommands.MemoHelp(self, ctx)
            elif ((ctx.message.content).lower().startswith("x!help tictactoe")):
               await HelpCommands.TicTacToeHelp(self, ctx)
            elif ((ctx.message.content).lower().startswith("x!help flagguesser")):
               await HelpCommands.FlagGuesserHelp(self, ctx)
            elif ((ctx.message.content).lower().startswith("x!help mini")):
               await HelpCommands.MiniCommandsHelp(self, ctx)
            elif ((ctx.message.content).lower().startswith("x!help reddit")):
               await HelpCommands.RedditHelp(self, ctx)
            else:
                await HelpCommands.AllHelp(self, ctx)
        
            
    async def AllHelp(self, ctx):
        Embed = discord.Embed(title="All help Commands | " + str(ctx.author),
                              description=" ",
                              color=discord.Color.from_rgb(255, 255, 255))
      
        Embed.add_field(name="x!help Memo",
                        value="Shows list of Memo commands & what they do",
                        inline=False)
      
        Embed.add_field(name="x!help MiniCommands",
                        value="Shows list of Mini commands & what they do",
                        inline=False)
      
        Embed.add_field(name="x!help FlagGuesser",
                        value="Shows list of FlagGuesser commands & what they do",
                        inline=False)
    
        Embed.add_field(name="x!help TicTacToe",
                        value="Shows list of TicTacToe commands & what they do",
                        inline=False)
    
        Embed.add_field(name="x!help Reddit",
                        value="Shows list of Reddit commands & what they do",
                        inline=False)
      
        Embed.set_footer(text="『Xrbot』", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU")    
        await ctx.send(embed=Embed)

  
    async def GetHelp(self, ctx):
        Embed = discord.Embed(title="Get Commands | " + str(ctx.author),
                              description=" ",
                              color=discord.Color.from_rgb(255, 255, 255))
      
        Embed.add_field(name="x!get lyrics [artist] [song]",
                        value="Shows lyrics of [song] by [artist]",
                        inline=False)
    
        Embed.add_field(name="x!get weather [country] [city]",
                        value="Shows weather for next 6 hours of [city] in [country]",
                        inline=False)
      
        Embed.set_footer(text="『Xrbot』", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU")
    
        await ctx.send(embed=Embed)

      
    async def MemoHelp(self, ctx):  # Prints list of Memo commands & what they do
        Embed = discord.Embed(title="Memo Commands | " + str(ctx.author),
                              description=" ",
                              color=discord.Color.from_rgb(255, 245, 93))
      
        Embed.add_field(name="x!memo add [Memo]",
                        value=" Adds [Memo] to list of memos",
                        inline=False)
      
        Embed.add_field(name="x!memo remove [Memo Number]",
                        value="Removes memo [Memo Number]",
                        inline=False)
      
        Embed.add_field(name="x!memo view [Memo Number]",
                        value="Shows memo [Memo Number]",
                        inline=False)
      
        Embed.add_field(name="x!memo view all",
                        value="Shows all memos",
                        inline=False)
    
        Embed.set_footer(text="『Xrbot』", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU")    
      
        await ctx.send(embed=Embed)
    
    
    async def MiniCommandsHelp(self, ctx):  # Prints list of Mini commands & what they do
        Embed = discord.Embed(title="Mini Commands | " + str(ctx.author),
                              description=" ",
                              color=discord.Color.from_rgb(198, 195, 255))
              
        Embed.add_field(name=" x!cf",
                        value="Flips a coin ",
                        inline=False)

        Embed.add_field(name="x!move [num] [channel]",
                        value="Purges the last [num] messages and moves them to [channel]",
                        inline=False)

        Embed.add_field(name="x!purge [num]",
                        value="Purges the last [num] messages",
                        inline=False)
      
        Embed.add_field(name="x!Penguroll",
                        value="Shows a random Pengu",
                        inline=False)
              
        Embed.add_field(name="x!random [Num1] [Num2]",
                        value="Pick a number between [Num1] [Num2] (Num2 = 0 if not specificed)",
                        inline=False)
              
        Embed.add_field(name="x!bs [Particant 1]  [Particant 2].... [Participant n]",
                        value="Spins a bottle and shows who its pointing to and from",
                        inline=False)

        Embed.add_field(name="x!poll [Question] - [option 1] - [option 2] - .... - [option n]",
                        value="Sends a reaction poll message (Max options are 9)",
                        inline=False)
      
        Embed.set_footer(text="『Xrbot』", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU")    
      
        await ctx.send(embed=Embed)
    
    
    async def FlagGuesserHelp(self,ctx):  # Prints list of FlagGuesser commands & what they do
        Embed = discord.Embed(title="FlagGuesser Commands | " + str(ctx.author),
                              description=" ",
                              color=discord.Color.from_rgb(0, 136, 35))
      
        Embed.add_field(name="x!flagguesser start | x!fg start",
                        value="Starts a game of FlagGuesser",
                        inline=False)
      
        Embed.add_field(name="x!flagguesser guess [Guess number] | x!fg guess [Guess number]",
                        value="Submits country number [#] as your answer",
                        inline=False)
      
        Embed.add_field(name="x!flagguesser end | x!fg end",
                        value="Ends the ongoing game of FlagGuesser",
                        inline=False)
    
        Embed.set_footer(text="『Xrbot』", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU")    
      
        await ctx.send(embed=Embed)
    
    
    async def TicTacToeHelp(self, ctx):  # Prints list of TicTacToe commands & what they do
        Embed = discord.Embed(title="TicTacToe Commands | " + str(ctx.author),
                              description=" ",
                              color=discord.Color.from_rgb(255, 153, 249))
              
        Embed.add_field(name="x!TicTacToe start [user]", 
                        value="Start a game of TicTacToe vs [user] or vs the bot if user not specified",
                        inline=False)
              
        Embed.add_field(name="x!tictactoe play [slot #]",
                        value="Places a piece in slot [slot #]",
                        inline=False)
              
        Embed.add_field(name="x!accept",
                        value="Accepts TicTacToe match request",
                        inline=False)
              
        Embed.add_field(name="x!reject",
                        value="Rejects TicTacToe match request",
                        inline=False)
              
        Embed.add_field(name="x!TicTacToe end",
                        value="Ends ongoing TicTacToe match",
                        inline=False)
    
        Embed.set_footer(text="『Xrbot』", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU")    
      
        await ctx.send(embed=Embed)
    
    
    async def RedditHelp(self, ctx):  # Prints list of Reddit commands & what they do
        Embed = discord.Embed(title="Reddit Commands | " + str(ctx.author),
                              description=" ",
                              color=discord.Color.from_rgb(255, 162, 162))
      
        Embed.add_field(name="x!reddit view [Reddit Username]",
                        value="Shows info of Reddit user",
                        inline=False)
      
        Embed.add_field(name="x!reddit sub [Subreddit name]",
                        value="Shows info of Subreddit",
                        inline=False)
      
        Embed.add_field(name="x!reddit [Category] [Subreddit] [Post #]",
                        value="Shows [Post #] in [Category] of [Subreddit]",
                        inline=False)
    
        Embed.set_footer(text="『Xrbot』", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU")    
      
        await ctx.send(embed=Embed)


async def setup(bot):
  await bot.add_cog(HelpCommands(bot))