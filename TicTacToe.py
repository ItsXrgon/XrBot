#Functions of the commands related to the TicTacToe features of the bot
import discord
import os
from PIL import Image
import random
import numpy as np
from discord.ext import commands
import HelpCommands


class TicTacToe(commands.Cog):
    def __init__(self, bot):
         self.bot = bot 
         self.games = {}


    @commands.command(name="tictactoe")
    async def Aliases(self, ctx):
        if (ctx.message.content).lower().startswith("x!tictactoe start "):
            await TicTacToe.TicTacToeVerify(self, ctx)
        elif (ctx.message.content).lower().startswith("x!tictactoe start"):
            await TicTacToe.TicTacToeStart(self, ctx)
        elif (ctx.message.content).lower().startswith("x!tictactoe play "):
            await TicTacToe.TicTacToePlay(self, ctx)
        elif(ctx.message.content).lower().startswith("x!tictactoe end"):
            await TicTacToe.EndGame(self, ctx)
        elif ((ctx.message.content).lower().startswith("x!tictactoe accept")
              or (ctx.message.content).lower().startswith("x!tictactoe reject")):
            await TicTacToe.TicTacToeCheck(self, ctx)
        else:
            await HelpCommands.HelpCommands.TicTacToeHelp(self, ctx)

  
    async def PrintBoard(self, ctx):  # Sends an image with the current board
        array = np.array( self.games[ctx.channel.id].pixels, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save("TicTacToe.png")  # Saves image as png
        await ctx.send(file=discord.File("TicTacToe.png"))
        os.remove("TicTacToe.png")  # Deletes image
    
    
    def SlotLocator(self, ctx):  # Takes slot number on the TicTacToe grid and returns the row & column of it
        if ((self.games[ctx.channel.id].Slot == 1) or ( self.games[ctx.channel.id].Slot == 2) or ( self.games[ctx.channel.id].Slot == 3)):
            Row = 0
        elif ((self.games[ctx.channel.id].Slot == 4) or ( self.games[ctx.channel.id].Slot == 5) or ( self.games[ctx.channel.id].Slot == 6)):
            Row = 1
        elif ((self.games[ctx.channel.id].Slot == 7) or ( self.games[ctx.channel.id].Slot == 8) or ( self.games[ctx.channel.id].Slot == 9)):
            Row = 2
        if ((self.games[ctx.channel.id].Slot == 1) or ( self.games[ctx.channel.id].Slot == 4) or ( self.games[ctx.channel.id].Slot == 7)): 
            Col = 0
        elif ((self.games[ctx.channel.id].Slot == 2) or ( self.games[ctx.channel.id].Slot == 5) or ( self.games[ctx.channel.id].Slot == 8)):
            Col = 1
        elif ((self.games[ctx.channel.id].Slot == 3) or ( self.games[ctx.channel.id].Slot == 6) or ( self.games[ctx.channel.id].Slot == 9)):
            Col = 2
        return [Row, Col]
    
    
    def DrawX(self, ctx):  # Draws X where player has selected
        Row, Col = TicTacToe.SlotLocator(self, ctx)
        i = 0
        for y in range(20, 80):
            for x in range(20, 80):
                if x == y or x - y == 60 - i * 2:
                    corrected_y = y + (Row * 100)
                    corrected_x = x + (Col * 100)
                    self.games[ctx.channel.id].pixels[corrected_y][corrected_x] = (255, 255, 255)
            i += 1
        self.games[ctx.channel.id].TicTacToe[self.games[ctx.channel.id].Slot-1] = 1
        self.games[ctx.channel.id].Turn += 1
      
      
    def DrawO(self, ctx):  # Draws O where player has selected
        Row, Col = TicTacToe.SlotLocator(self, ctx)
        for y in range(100):
            for x in range(100):
                calc_x = x
                calc_y = y
                if calc_x == 50:
                    calc_x = 0
                else:
                    calc_x = calc_x - 50
          
                if calc_y == 50:
                    calc_y = 0
                else:
                    calc_y = calc_y - 50
                squared = pow(calc_x, 2) + pow(calc_y, 2)
                if squared < 100 * 8 + 30 and squared > 100 * 8 - 30:
                    corrected_y = y + (Row * 100)
                    corrected_x = x + (Col * 100)
                    self.games[ctx.channel.id].pixels[corrected_y][corrected_x] = (255, 255, 255)
        self.games[ctx.channel.id].TicTacToe[ self.games[ctx.channel.id].Slot-1] = 0
        self.games[ctx.channel.id].Turn += 1
      
    
    async def BotTurn(self, ctx):  # Analyzes current board and pics best possible move
        # Checks if an immediate win is possible over the need for a block
        if (((self.games[ctx.channel.id].TicTacToe[1] == 0 and  self.games[ctx.channel.id].TicTacToe[2] == 0) or
             (self.games[ctx.channel.id].TicTacToe[3] == 0 and  self.games[ctx.channel.id].TicTacToe[6] == 0) or
             (self.games[ctx.channel.id].TicTacToe[4] == 0 and  self.games[ctx.channel.id].TicTacToe[8] == 0)) and  self.games[ctx.channel.id].TicTacToe[0] == 2):
            self.games[ctx.channel.id].Slot = 1
        elif (((self.games[ctx.channel.id].TicTacToe[0] == 0 and  self.games[ctx.channel.id].TicTacToe[2] == 0) or
             (self.games[ctx.channel.id].TicTacToe[4] == 0 and  self.games[ctx.channel.id].TicTacToe[7] == 0)) and  self.games[ctx.channel.id].TicTacToe[1] == 2):
            self.games[ctx.channel.id].Slot = 2
        elif (((self.games[ctx.channel.id].TicTacToe[0] == 0 and  self.games[ctx.channel.id].TicTacToe[1] == 0) or
             (self.games[ctx.channel.id].TicTacToe[5] == 0 and  self.games[ctx.channel.id].TicTacToe[8] == 0) or
             (self.games[ctx.channel.id].TicTacToe[4] == 0 and  self.games[ctx.channel.id].TicTacToe[6] == 0)) and  self.games[ctx.channel.id].TicTacToe[2] == 2):
            self.games[ctx.channel.id].Slot = 3
        elif (((self.games[ctx.channel.id].TicTacToe[4] == 0 and  self.games[ctx.channel.id].TicTacToe[5] == 0) or
             (self.games[ctx.channel.id].TicTacToe[0] == 0 and  self.games[ctx.channel.id].TicTacToe[6] == 0)) and  self.games[ctx.channel.id].TicTacToe[3] == 2):
             self.games[ctx.channel.id].Slot = 4
        elif (((self.games[ctx.channel.id].TicTacToe[3] == 0 and  self.games[ctx.channel.id].TicTacToe[5] == 0) or
             (self.games[ctx.channel.id].TicTacToe[1] == 0 and  self.games[ctx.channel.id].TicTacToe[7] == 0)) and  self.games[ctx.channel.id].TicTacToe[4] == 2):
            self.games[ctx.channel.id].Slot = 5
        elif (((self.games[ctx.channel.id].TicTacToe[3] == 0 and  self.games[ctx.channel.id].TicTacToe[4] == 0) or
             (self.games[ctx.channel.id].TicTacToe[2] == 0 and  self.games[ctx.channel.id].TicTacToe[8] == 0)) and  self.games[ctx.channel.id].TicTacToe[5] == 2):
            self.games[ctx.channel.id].Slot = 6
        elif (((self.games[ctx.channel.id].TicTacToe[4] == 0 and  self.games[ctx.channel.id].TicTacToe[2] == 0) or
             (self.games[ctx.channel.id].TicTacToe[7] == 0 and  self.games[ctx.channel.id].TicTacToe[8] == 0) or
             (self.games[ctx.channel.id].TicTacToe[0] == 0 and  self.games[ctx.channel.id].TicTacToe[3] == 0)) and  self.games[ctx.channel.id].TicTacToe[6] == 2):
            self.games[ctx.channel.id].Slot = 7
        elif (((self.games[ctx.channel.id].TicTacToe[6] == 0 and  self.games[ctx.channel.id].TicTacToe[8] == 0) or
             (self.games[ctx.channel.id].TicTacToe[1] == 0 and  self.games[ctx.channel.id].TicTacToe[4] == 0)) and  self.games[ctx.channel.id].TicTacToe[7] == 2):
            self.games[ctx.channel.id].Slot = 8
        elif (((self.games[ctx.channel.id].TicTacToe[6] == 0 and  self.games[ctx.channel.id].TicTacToe[7] == 0) or
             (self.games[ctx.channel.id].TicTacToe[5] == 0 and  self.games[ctx.channel.id].TicTacToe[2] == 0) or
             (self.games[ctx.channel.id].TicTacToe[0] == 0 and  self.games[ctx.channel.id].TicTacToe[4] == 0)) and  self.games[ctx.channel.id].TicTacToe[8] == 2):
            self.games[ctx.channel.id].Slot = 9
               
        # Checks if an immediate block is needed 
        elif (((self.games[ctx.channel.id].TicTacToe[1] == 1 and  self.games[ctx.channel.id].TicTacToe[2] == 1) or
             (self.games[ctx.channel.id].TicTacToe[3] == 1 and  self.games[ctx.channel.id].TicTacToe[6] == 1) or
             (self.games[ctx.channel.id].TicTacToe[4] == 1 and  self.games[ctx.channel.id].TicTacToe[8] == 1)) and  self.games[ctx.channel.id].TicTacToe[0] == 2):
             self.games[ctx.channel.id].Slot = 1            
        elif (((self.games[ctx.channel.id].TicTacToe[0] == 1 and  self.games[ctx.channel.id].TicTacToe[2] == 1) or
             (self.games[ctx.channel.id].TicTacToe[4] == 1 and  self.games[ctx.channel.id].TicTacToe[7] == 1)) and  self.games[ctx.channel.id].TicTacToe[1] == 2):
             self.games[ctx.channel.id].Slot = 2
        elif (((self.games[ctx.channel.id].TicTacToe[0] == 1 and  self.games[ctx.channel.id].TicTacToe[1] == 1) or
             (self.games[ctx.channel.id].TicTacToe[5] == 1 and  self.games[ctx.channel.id].TicTacToe[8] == 1) or
             (self.games[ctx.channel.id].TicTacToe[4] == 1 and  self.games[ctx.channel.id].TicTacToe[6] == 1)) and  self.games[ctx.channel.id].TicTacToe[2] == 2):
             self.games[ctx.channel.id].Slot = 3
        elif (((self.games[ctx.channel.id].TicTacToe[4] == 1 and  self.games[ctx.channel.id].TicTacToe[5] == 1) or
             (self.games[ctx.channel.id].TicTacToe[0] == 1 and  self.games[ctx.channel.id].TicTacToe[6] == 1)) and  self.games[ctx.channel.id].TicTacToe[3] == 2):
             self.games[ctx.channel.id].Slot = 4
        elif (((self.games[ctx.channel.id].TicTacToe[3] == 1 and  self.games[ctx.channel.id].TicTacToe[5] == 1) or
             (self.games[ctx.channel.id].TicTacToe[1] == 1 and  self.games[ctx.channel.id].TicTacToe[7] == 1)) and  self.games[ctx.channel.id].TicTacToe[4] == 2):
             self.games[ctx.channel.id].Slot = 5
        elif (((self.games[ctx.channel.id].TicTacToe[3] == 1 and  self.games[ctx.channel.id].TicTacToe[4] == 1) or
             (self.games[ctx.channel.id].TicTacToe[2] == 1 and  self.games[ctx.channel.id].TicTacToe[8] == 1)) and  self.games[ctx.channel.id].TicTacToe[5] == 2):
             self.games[ctx.channel.id].Slot = 6
        elif (((self.games[ctx.channel.id].TicTacToe[4] == 1 and  self.games[ctx.channel.id].TicTacToe[2] == 1) or
             (self.games[ctx.channel.id].TicTacToe[7] == 1 and  self.games[ctx.channel.id].TicTacToe[8] == 1) or
             (self.games[ctx.channel.id].TicTacToe[0] == 1 and  self.games[ctx.channel.id].TicTacToe[3] == 1)) and  self.games[ctx.channel.id].TicTacToe[6] == 2):
             self.games[ctx.channel.id].Slot = 7
        elif (((self.games[ctx.channel.id].TicTacToe[6] == 1 and  self.games[ctx.channel.id].TicTacToe[8] == 1) or
             (self.games[ctx.channel.id].TicTacToe[1] == 1 and  self.games[ctx.channel.id].TicTacToe[4] == 1)) and  self.games[ctx.channel.id].TicTacToe[7] == 2):
             self.games[ctx.channel.id].Slot = 8
        elif (((self.games[ctx.channel.id].TicTacToe[6] == 1 and  self.games[ctx.channel.id].TicTacToe[7] == 1) or
             (self.games[ctx.channel.id].TicTacToe[5] == 1 and  self.games[ctx.channel.id].TicTacToe[2] == 1) or
             (self.games[ctx.channel.id].TicTacToe[0] == 1 and  self.games[ctx.channel.id].TicTacToe[4] == 1)) and  self.games[ctx.channel.id].TicTacToe[8] == 2):
             self.games[ctx.channel.id].Slot = 9             

        if( self.games[ctx.channel.id].Slot == None):  # if no block or win possible, picks best possible slot       
            # Sequence if Player 1 stared on center      
            if (self.games[ctx.channel.id].StartingSlot == 5):  
              if (self.games[ctx.channel.id].Turn == 1):
                  possible_placements = [1, 3, 6, 8]
                  self.games[ctx.channel.id].Slot = possible_placements[random.randint(0, 3)]
        
              if (self.games[ctx.channel.id].Turn == 3 or  self.games[ctx.channel.id].Turn == 5 
                  or  self.games[ctx.channel.id].Turn == 7 or  self.games[ctx.channel.id].Turn == 9):
                  possible_placements = [2, 4, 6, 8]
                  self.games[ctx.channel.id].Slot = possible_placements[random.randint(0, 3)]
                  while (self.games[ctx.channel.id].TicTacToe[ self.games[ctx.channel.id].Slot - 1] != 2 and  self.games[ctx.channel.id].TicTacToe[self.games[ctx.channel.id].Slot - 1] != 1):
                       self.games[ctx.channel.id].Slot = possible_placements[random.randint(0, 3)]
                    
            # Sequence if Player 1 stared on a corner
            elif (self.games[ctx.channel.id].StartingSlot == 7 or  self.games[ctx.channel.id].StartingSlot == 9
                  or  self.games[ctx.channel.id].StartingSlot == 1 or  self.games[ctx.channel.id].StartingSlot == 3): 
                if ( self.games[ctx.channel.id].Turn == 1):
                     self.games[ctx.channel.id].Slot = 5
        
                if (self.games[ctx.channel.id].Turn == 3 or  self.games[ctx.channel.id].Turn == 5 
                    or  self.games[ctx.channel.id].Turn == 7 or  self.games[ctx.channel.id].Turn == 9):
                    possible_placements = [2, 4, 6, 8]
                    self.games[ctx.channel.id].Slot = possible_placements[random.randint(0, 3)]
                    while ( self.games[ctx.channel.id].TicTacToe[ self.games[ctx.channel.id].Slot - 1] != 2 and  self.games[ctx.channel.id].TicTacToe[ self.games[ctx.channel.id].Slot - 1] != 1):
                         self.games[ctx.channel.id].Slot = possible_placements[random.randint(0, 3)]
                      
            # Sequence if Player 1 stared on an edge
            elif (self.games[ctx.channel.id].StartingSlot == 2 or  self.games[ctx.channel.id].StartingSlot == 4 or  self.games[ctx.channel.id].StartingSlot == 6 or  self.games[ctx.channel.id].StartingSlot == 8):  
                if (self.games[ctx.channel.id].Turn == 1):
                     self.games[ctx.channel.id].Slot = 5
                  
                if (self.games[ctx.channel.id].Turn == 3):
                    if ((self.games[ctx.channel.id].TicTacToe[2] == 1 and  self.games[ctx.channel.id].TicTacToe[8] == 1)
                            or ( self.games[ctx.channel.id].TicTacToe[4] == 1 and  self.games[ctx.channel.id].TicTacToe[6] == 1)):
                        possible_placements = [1, 3, 7, 9]
                        self.games[ctx.channel.id].Slot = possible_placements[random.randint(0, 3)]
                        while ( self.games[ctx.channel.id].TicTacToe[ self.games[ctx.channel.id].Slot - 1] != 2 and  self.games[ctx.channel.id].TicTacToe[ self.games[ctx.channel.id].Slot - 1] != 1):
                             self.games[ctx.channel.id].Slot = possible_placements[random.randint(0, 3)]
            
        await ctx.send(f"Xrbot chooses to play in slot # {str( self.games[ctx.channel.id].Slot)}")
        TicTacToe.DrawO(self, ctx)
        await TicTacToe.PrintBoard(self, ctx)
    
    
    async def TicTacToeBot(self, ctx):  # Draws the X&Os, passes the turn to player/bot till game ends    
        if (self.games[ctx.channel.id].Players != "" and  self.games[ctx.channel.id].Turn % 2== 1):  #  If True then player 2 is playing vs player 1
            await ctx.send(f"{str(ctx.author)} has chosen slot #{str( self.games[ctx.channel.id].Slot)}")
            TicTacToe.DrawO(self, ctx)
            await TicTacToe.PrintBoard(self, ctx)
            await TicTacToe.VictoryCheck(self, ctx)
            try:  # Checks if game ended
                self.games[ctx.channel.id]
            except:
                return
            await ctx.send("Your turn " +  self.games[ctx.channel.id].Players[1])
          
        elif ( self.games[ctx.channel.id].Players != "" and  self.games[ctx.channel.id].Turn % 2 == 0):  #  If True then player 1 is playing vs player 2
            await ctx.send(f"{str(ctx.author)} has chosen slot #{str( self.games[ctx.channel.id].Slot)}")
            TicTacToe.DrawX(self, ctx)
            await TicTacToe.PrintBoard(self, ctx)
            await TicTacToe.VictoryCheck(self, ctx)
            try:  # Checks if game ended
                self.games[ctx.channel.id]
            except:
                return
            await ctx.send(f"Your turn { self.games[ctx.channel.id].Players[0]}")
          
        elif(self.games[ctx.channel.id].Turn==9):
            await ctx.send("Game has ended in a draw")
            await TicTacToe.EndGame(self, ctx)
                                    
        else: #  then player 1 plays vs bot then bot plays
            await ctx.send(f"{str(ctx.author)} has chosen slot #{str( self.games[ctx.channel.id].Slot)}")
            TicTacToe.DrawX(self, ctx)
            await TicTacToe.PrintBoard(self, ctx)
            await TicTacToe.VictoryCheck(self, ctx)
            try:  # Checks if game ended
                self.games[ctx.channel.id]
            except:
                return
            
            if(self.games[ctx.channel.id].Turn==9):
                await ctx.send("Game has ended in a draw")
                await TicTacToe.EndGame(self, ctx) 
              
            self.games[ctx.channel.id].Slot = None
            await TicTacToe.BotTurn(self, ctx)
            await TicTacToe.VictoryCheck(self, ctx)

          
    async def TicTacToePlay(self, ctx):
    # Gets slot number from message, verifies turn & keeps passing turns till the game ends
        if (self.games[ctx.channel.id].Players != ""):  # If True then game is player vs player
            if (self.games[ctx.channel.id].Turn % 2 == 0):  # Player 2"s turn
                if (ctx.author.mention != str( self.games[ctx.channel.id].Players[1])):  # Checks if command came from player 2
                    await ctx.send("Not your turn yet!")
                    return
                  
            elif (self.games[ctx.channel.id].Turn % 2 == 1):  # Player 1"s turn
                if (ctx.author.mention != str( self.games[ctx.channel.id].Players[0])):  # Checks if command came from player 1
                    await ctx.send("Not your turn yet!")
                    return
                  
        self.games[ctx.channel.id].Slot = ctx.message.content.lower().split("x!tictactoe play ")[1]
        try:  # Checks input is an integer and not a string
            self.games[ctx.channel.id].Slot = int( self.games[ctx.channel.id].Slot)
        except:
            await ctx.send("Incorrect format\nx!tictactoe play [slot #]")
            return
          
        if(self.games[ctx.channel.id].Slot<1 or  self.games[ctx.channel.id].Slot>9):
            await ctx.send("Incorrect format\nx!tictactoe play [slot #]")
            return
              
        if (self.games[ctx.channel.id].TicTacToe[ self.games[ctx.channel.id].Slot - 1] != 2):
            await ctx.send("Slot taken, select another one!")
            return
    
        if (self.games[ctx.channel.id].Turn == 0):  # Decides the reactionary sequence the bot should choose 
             self.games[ctx.channel.id].StartingSlot =  self.games[ctx.channel.id].Slot
                           
        try:
          self.games[ctx.channel.id]  # If game is ongoing and turn is valid, place the pieces
        except:
          await ctx.send("x!tictactoe start [user] to play vs a friend or x!tictactoe start to play vs『Xrbot』")

        else:
          await TicTacToe.TicTacToeBot(self, ctx)




    async def TicTacToeVerify(self, ctx):  # Asks if the 2nd player is willing to participate in the match
        try:  # Checks if there is an ongoing game already
            self.games[ctx.channel.id]
        except:
            self.games[ctx.channel.id] = TicTacToeGame()
        try:
            ctx.message.mentions[0]
        except:
            Player2 = ctx.message.content.lower().replace("x!tictactoe start ", "")
            await ctx.send(f"{Player2} is mot a valid user")
            return
        
        self.games[ctx.channel.id].Players = [ctx.author.mention, ctx.message.mentions[0]]
        await ctx.send(f"{self.games[ctx.channel.id].Players[1].mention}, you have been challanged to a TicTacToe match by { self.games[ctx.channel.id].Players[0]} accept/reject by ```x!tictactoe accept\nx!tictactoe reject```")
    

    async def TicTacToeCheck(self, ctx):
        try:  # Checks if there is an ongoing game already
            self.games[ctx.channel.id]
            self.games[ctx.channel.id].Players[0]
        except:
            await ctx.send("No ongoing game request to accept or reject")
            return
        if(self.games[ctx.channel.id].Players[0] == ctx.author.mention):
            await ctx.send("TicTacToe game starting!")
            await ctx.send(f"You may start 1st {ctx.author.mention} Type x!Tictactoe play [slot #] Starting from slot 1 on top left square to slot 9 on bottom right")
            await TicTacToe.PrintBoard(self, ctx)
        else:
             await ctx.send("No ongoing game request to you")

  
    async def TicTacToeStart(self, ctx):  # Initializes databases and starts the game

        try:  # Checks if there is an ongoing game already
            self.games[ctx.channel.id]
        except:
            self.games[ctx.channel.id] = TicTacToeGame()
            await ctx.send("TicTacToe game starting!")
            await ctx.send(f"You may start 1st {ctx.author.mention} Type x!Tictactoe play [slot #] Starting from slot 1 on top left square to slot 9 on bottom right")
            await TicTacToe.PrintBoard(self, ctx)
        else: 
            await ctx.send("TicTacToe already in progress!")

  
    async def EndGame(self, ctx):  # Ends game
        try:
             self.games[ctx.channel.id]
        except:
            await ctx.send("No current TicTacToe in progress!")
        else: 
            await  ctx.send("Game has ended!")
            del  self.games[ctx.channel.id]

  
    async def GameOver(self, ctx):
        if (self.games[ctx.channel.id].Players != ""):
            if (self.games[ctx.channel.id].Turn % 2 == 0):   # If game is player vs player
                result = self.games[ctx.channel.id].Players[0]  # If game ended at even turn number, player 1 wins
            else:
                result = self.games[ctx.channel.id].Players[1]  # If game ended at odd turn number, player 2 wins
        else:
            if (self.games[ctx.channel.id].Turn % 2 == 1):  # If game ended at even turn number, player 1 wins vs bot
                result = str(ctx.author)
            else:
                result = "『Xrbot』"  # Else bot wins
        await ctx.send(f"GAME OVER! {result} has won in {str( self.games[ctx.channel.id].Turn)} turns!\n")
        await TicTacToe.EndGame(self, ctx)

    
    async def VictoryCheck(self,ctx):  # Checks if there are any 3 identical adjacanet slots
            def HorizontalVictory(self, ctx):
                if (self.games[ctx.channel.id].TicTacToe[0] ==  self.games[ctx.channel.id].TicTacToe[1] ==  self.games[ctx.channel.id].TicTacToe[2] != 2):
                    line = 1
                elif (self.games[ctx.channel.id].TicTacToe[3] ==  self.games[ctx.channel.id].TicTacToe[4] ==  self.games[ctx.channel.id].TicTacToe[5] != 2):
                    line = 3
                elif (self.games[ctx.channel.id].TicTacToe[6] ==  self.games[ctx.channel.id].TicTacToe[7] ==  self.games[ctx.channel.id].TicTacToe[8] != 2):
                    line = 5
                for i in range(300):
                     self.games[ctx.channel.id].pixels[50*line][i] = (255, 255, 255)
        
            def VerticalVictory(self, ctx):
                if (self.games[ctx.channel.id].TicTacToe[0] ==  self.games[ctx.channel.id].TicTacToe[3] ==  self.games[ctx.channel.id].TicTacToe[6] != 2):
                    line = 1
                elif (self.games[ctx.channel.id].TicTacToe[1] ==  self.games[ctx.channel.id].TicTacToe[4] ==  self.games[ctx.channel.id].TicTacToe[7] != 2):
                    line = 3
                elif (self.games[ctx.channel.id].TicTacToe[2] ==  self.games[ctx.channel.id].TicTacToe[5] ==  self.games[ctx.channel.id].TicTacToe[8] != 2):
                    line = 5
                for i in range(300):
                     self.games[ctx.channel.id].pixels[i][50*line] = (255, 255, 255)
              
            if ((self.games[ctx.channel.id].TicTacToe[0] ==  self.games[ctx.channel.id].TicTacToe[1] ==  self.games[ctx.channel.id].TicTacToe[2] != 2)
                or (self.games[ctx.channel.id].TicTacToe[3] ==  self.games[ctx.channel.id].TicTacToe[4] ==  self.games[ctx.channel.id].TicTacToe[5] != 2)
                or(self.games[ctx.channel.id].TicTacToe[6] ==  self.games[ctx.channel.id].TicTacToe[7] ==  self.games[ctx.channel.id].TicTacToe[8] != 2)):  # Checks if game is over
                HorizontalVictory(self, ctx)
                await TicTacToe.PrintBoard(self, ctx)
                await TicTacToe.GameOver(self, ctx)
                  
            elif ((self.games[ctx.channel.id].TicTacToe[0] ==  self.games[ctx.channel.id].TicTacToe[3] ==  self.games[ctx.channel.id].TicTacToe[6] != 2)
                or (self.games[ctx.channel.id].TicTacToe[1] ==  self.games[ctx.channel.id].TicTacToe[4] ==  self.games[ctx.channel.id].TicTacToe[7] != 2)
                or (self.games[ctx.channel.id].TicTacToe[2] ==  self.games[ctx.channel.id].TicTacToe[5] ==  self.games[ctx.channel.id].TicTacToe[8] != 2)):  # Checks if game is over
                VerticalVictory(self, ctx)
                await TicTacToe.PrintBoard(self, ctx)
                await TicTacToe.GameOver(self, ctx)
                  
            elif (self.games[ctx.channel.id].TicTacToe[2] ==  self.games[ctx.channel.id].TicTacToe[4] ==  self.games[ctx.channel.id].TicTacToe[6] != 2):  # Checks if game is over
                j = 300
                for i in range(300):
                    j-=1
                    self.games[ctx.channel.id].pixels[j][i] = (255, 255, 255)
                    
                await TicTacToe.PrintBoard(self, ctx)
                await TicTacToe.GameOver(self, ctx)
              
            elif ( self.games[ctx.channel.id].TicTacToe[0] ==  self.games[ctx.channel.id].TicTacToe[4] ==  self.games[ctx.channel.id].TicTacToe[8] != 2):  # Checks if game is over
                j = 0
                for i in range(300):
                    self.games[ctx.channel.id].pixels[j][i] = (255, 255, 255)
                    j+=1
                await TicTacToe.PrintBoard(self, ctx)
                await TicTacToe.GameOver(self, ctx)             


class TicTacToeGame:
    def __init__(self):
        self.pixels = [[(0, 0, 0) for _ in range(300)]  for _ in range(300)]
        for i in range(2):
          for x in range(300):
              self.pixels[x][100*(i+1)] = (255, 255, 255)
              self.pixels[100*(i+1)][x] = (255, 255, 255)
          
        self.TicTacToe = [2,2,2,2,2,2,2,2,2]  # 2 signifies an empty slot, 1 a slot with X and 0 a slot with O
        self.Turn = 0
        self.Players = ""
        self.StartingSlot = None
