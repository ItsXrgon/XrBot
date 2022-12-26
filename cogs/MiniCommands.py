#Functions of the commands related to the MiniCommands features of the bot
import random
import discord
from discord import app_commands
from discord.ext import commands
import os


class MiniCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def setup(bot: commands.Bot) -> None:
      await bot.add_cog(
        MiniCommands(bot),
        guilds = [discord.Object(id="1033487447885103244")]
      )
      
    @commands.command(name="random")
    async def NumberBetween(self, ctx):  # Gets random number between 2 inputs
        Num = ctx.message.content.lower().replace("x!random ", "").split()
        try:  # Checks inputs are integers and not strings
            Num_1 = int(Num[0])
            Num_2 = int(Num[1])
        except:
            await ctx.send("Incorrect format\nx!random [Num1] [Num2]")
            return
      
        if (number1 > number2):
            Max = number1
            Min = number2
        else:
            Max = number2
            Min = number1
        Random = str(random.randint(Min, Max))
        Result = f"Random number between {Min} & {Max} is {Random}"

        await interaction.response.send_message(Result)

    @commands.command(name="cf")
    async def CoinFlip(self, ctx):  # Flips a coin
        Result = "Heads" if (random.randint(0, 1) == 1) else "Tails"
        await ctx.send(Result)

    @commands.command(name="bs")
    async def SpinTheBottle(
            self, ctx):  # Spins a bottle and gives who its pointing to & from
        # forms a list of the user inputted participants
        Particpants = ctx.message.content.lower().replace("x!bs ","").split()

        # bottle pointing to
        BottleFront = Particpants[random.randint(0, len(Particpants) - 1)]

        # bottle pointing from
        BottleBack = Particpants[random.randint(0, len(Particpants) - 1)]

        # incase front and back point at same participant
        while (BottleFront == BottleBack):
            BottleBack = Particpants[random.randint(0, len(Particpants) - 1)]

        Result = f"bottle has been spun and is now pointing at {BottleFront} from {BottleBack}"
        await ctx.send(Result)

    @commands.command(name="poll")
    async def poll(self, ctx):  # Flips a coin
        PollOptions = ctx.message.content.replace("x!poll ", "").split('-')
        Question = PollOptions.pop(0)
        NumberOfOptions = len(PollOptions)
        if (NumberOfOptions > 9 or NumberOfOptions == 0):
            await ctx.send(
                "Incorrect format\nx!poll [Question] - [option 1] - [option 2] - .... - [option n]"
            )
            return
        else:
            result = ""
            for i in range(NumberOfOptions):
                result += f"{i+1}) {PollOptions[i]}\n"

            Embed = discord.Embed(title=f"{ctx.author} asks:\n{Question}",
                                  color=discord.Color.from_rgb(255, 144, 200))

            Embed.add_field(name="Poll options:", value=result, inline=False)

            Poll = await ctx.send(embed=Embed)
            PollNumbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            for i in range(NumberOfOptions):
                await Poll.add_reaction(PollNumbers[i])

    @commands.command(name="move")
    async def moveChat(self, ctx):
        try:
          messageNumber, channel = ctx.message.content.replace("x!move ", "").split()
          channel = self.bot.get_channel(int(channel.replace("<#","").replace(">","")))
          messages = await ctx.channel.history(limit=int(messageNumber)+1).flatten()
        except:
          await ctx.send("Incorrect format, do x!move [num] [channel]")
          return

        if(ctx.author.guild_permissions.manage_messages):
          i = len(messages)-1
          while(i>0):
            message = messages[i]
            i-=1
          await channel.send(f"{message.author.name}: {message.content}")
          j = 0
          while(j < len(message.attachments)):
              await channel.send(message.attachments[j].url)
              j += 1
          await ctx.channel.purge(limit=int(len(messages))+1)
      
    @commands.command(name="purge")
    async def purge(self, ctx):
        limit = ctx.message.content.split()[1]
        if(ctx.author.guild_permissions.manage_messages):
          try:
            int(limit)
          except:
            await ctx.send("Incorrect format, do x!purge [number of messages]")
            return
          await ctx.channel.purge(limit=int(limit)+1)


    @commands.command(name="PenguRoll")
    async def PenguRoll(self, ctx):  # Sends a random image of a penguin
        path = random.choice(os.listdir("PenguinImages/"))
        Pengu = discord.File("PenguinImages/" + path)
        PenguName = "***" + path.replace(".png", "") + "***"
        await ctx.send(PenguName, file=Pengu)

async def setup(bot):
  await bot.add_cog(MiniCommands(bot))