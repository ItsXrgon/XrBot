# Functions of the commands related to the Memo features of the bot
from discord.ext import commands
from cogs.help import HelpCommands


class MemoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="memo")
    async def Aliases(self, ctx):
        if str(ctx.author).startswith("『Xrgon』"):
            if (ctx.message.content).lower().startswith("x!memo add"):
                await MemoCommands.MemoAdd(self, ctx)
            elif (ctx.message.content).lower().startswith("x!memo remove"):
                await MemoCommands.MemoRemove(self, ctx)
            elif (ctx.message.content).lower().startswith("x!memo view all"):
                await MemoCommands.MemoViewAll(self, ctx)
            elif (ctx.message.content).lower().startswith("x!memo view"):
                await MemoCommands.MemoView(self, ctx)
            else:
                await HelpCommands.memo_help(ctx)

    async def MemoAdd(self, ctx):  # Add memo to database
        Memo = ctx.message.content.lower().replace("x!memo add ", "")
        if (
            "Memo" not in db.keys()
        ):  # Create database if there wasnt already and add memo
            db["Memo"] = [Memo]
        else:
            db["Memo"].append(Memo)
        MemoNum = len(db["Memo"])
        Result = f"Memo added - Memo number is # {str(MemoNum)}"
        await ctx.send(Result)

    async def MemoRemove(self, ctx):  # Remove memo from database
        MemoNumber = int(ctx.message.content.lower().replace("x!memo remove ", ""))
        try:  # Checks input is integer and not string
            int(MemoNumber)
        except:
            await ctx.send("Incorrect format\nx!memo remove [Memo Number]")
            return

        if len(ctx.message.content.split()) > 3 or MemoNumber < 0:
            await ctx.send("Incorrect format\nx!memo remove [Memo Number]")

        elif (
            "Memo" not in db.keys() or len(db["Memo"]) == 0
        ):  # Makes sure database exists
            await ctx.send("No current memos available to remove")
        elif len(db["Memo"]) < MemoNumber:  # Makes sure memo exits
            await ctx.send("Memo number is not available")
        else:
            RemovedMemo = db["Memo"].pop(MemoNumber - 1)  # Removes memo
            Result = f"Memo #{MemoNumber}\n{RemovedMemo} - removed"
            await ctx.send(Result)

    async def MemoViewAll(self, ctx):  # Shows all memos available on separate lines
        Result = "No current memos available to view"
        if not (
            "Memo" not in db.keys() or len(db["Memo"]) == 0
        ):  # Makes sure database exists
            Result = "Viewing all memos: \n"
            for i in range(1, len(db["Memo"]) + 1):
                Memo = db["Memo"][i - 1]
                Result += f"Memo #{i} - {Memo}\n"

        await ctx.send(Result)

    async def MemoView(self, ctx):  # Shows memo of given number
        MemoNumber = int(
            ctx.message.content.lower().split("x!memo view ", 1)[1]
        )  # Gets memo number from message sent
        try:  # Checks input is an integer and not a string
            int(MemoNumber)
        except:
            await ctx.send("Incorrect format\nx!memo view [Memo Number]")
            return

        if len(ctx.message.content.split()) > 3 or MemoNumber < 0:
            await ctx.send("Incorrect format\nx!memo view [Memo Number]")
        if (
            "Memo" not in db.keys() or len(db["Memo"]) == 0
        ):  # Makes sure database exists
            await ctx.send("No current memos available to view")
        elif len(db["Memo"]) < MemoNumber:  # checks if memo number is in list
            await ctx.send("Memo does not exist")
        else:
            Memo = db["Memo"][MemoNumber - 1]
            Result = f"Memo #{MemoNumber} - {Memo}"
            await ctx.send(Result)


async def setup(bot):
    await bot.add_cog(MemoCommands(bot))
