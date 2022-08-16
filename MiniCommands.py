#Functions of the commands related to the MiniCommands features of the bot
import random
import discord
from discord.ext import commands
import os


class MiniCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="random")
    async def NumberBetween(self, ctx):  # Gets random number between 2 inputs
        Num = ctx.message.content.lower().replace("x!random ", "").split()
        try:  # Checks inputs are integers and not strings
            Num_1 = int(Num[0])
            Num_2 = int(Num[1])
        except:
            await ctx.send("Incorrect format\nx!random [Num1] [Num2]")
            return
          
        if (Num_1 > Num_2):
            Max = Num_1
            Min = Num_2
        else:
            Max = Num_2
            Min = Num_1
        Random = str(random.randint(Min, Max))
        Result = f"Random number between {Min} & {Max} is {Random}"

        await ctx.send(Result)

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
