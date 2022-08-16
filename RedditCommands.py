#Functions of the Reddit features of the bot
import discord
from discord.ext import commands
import praw
from prawcore.exceptions import NotFound
from datetime import datetime
import HelpCommands

class RedditCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Reddit = praw.Reddit(client_id="7I8sxZgg68S2gLIwTNY1kw",
                         client_secret="FlHYr1vH0MjdsL4IDInDB4kWawvrmA",
                         user_agent="redditdev scraper by u/Xron-_-",
                         username="Xrbot-_-",
                         password="XrbotXrbot",
                         check_for_async=False)
        self.Thumbnail ="https://static.vecteezy.com/system/resources/thumbnails/008/385/732/small/reddit-social-media-icon-logo-abstract-symbol-illustration-free-vector.jpg"
        self.Logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpWjazsIH_jKlNjpzwxKfooH8DbLkon443XA&usqp=CAU"

  
    @commands.command(name="reddit")
    async def Aliases(self, ctx):
        if(ctx.message.content).lower().startswith("x!reddit "):
          if(ctx.message.content).lower().startswith("x!reddit view "):
               await RedditCommands.ViewUser(self, ctx)
          elif(ctx.message.content).lower().startswith("x!reddit sub "):
               await RedditCommands.SubredditView(self, ctx)
          elif(ctx.message.content).lower().startswith("x!reddit "):
               await RedditCommands.TopPost(self, ctx)
          else:
               await HelpCommands.RedditHelp(self, ctx)

          
    async def TopPost(self, ctx):  # Shows post in category & subreddit decided by user
        Input = ctx.message.content.lower().replace("x!reddit ", "").split()  # Gets the inputs     
        if (len(Input) == 3):  # if 3 inputs given checks validity
            try:  # Checks input 3 is an integer and not a string
                Input[2] = int(Input[2])
            except:
              await ctx.send(
                "Incorrect format, do x!reddit [category] [subreddit] [post #] ([post #] < 887)")
              return
  
            if(Input[2] < 887 and Input[2] > 0
            and (type(Input[0]) == type(Input[1]) == str)
            and (Input[0].lower() in ["top", "hot", "new", "rising"])): 
                  SubCategory = Input[0]
                  Subreddit = Input[1]
                  PostNumber = int(Input[2])
            else:
                await ctx.send(
              "Incorrect format, do x!reddit [category] [subreddit] [post #] ([post #] < 887)")
                return
              
        elif (len(Input) == 2  # if 2 inputs given checks validity
            and (type(Input[0]) == type(Input[1]) == str)
            and (Input[0].lower() in ["top", "hot", "new", "rising"])):  # if 2 inputs given
            SubCategory = Input[0]
            Subreddit = Input[1]
            PostNumber = 1
        else:
            await ctx.send(
                "Incorrect format, do x!reddit [category] [subreddit] [post #] ([post #] < 887)")
            return
    
        # Checks if Subreddit exists
        try:
            self.Reddit.subreddits.search_by_name(Subreddit, exact=True)
        except NotFound:  # if Subreddit doesnt exist, returns
            await ctx.send(f"Subreddit r/{Subreddit} does not exist")
            return
    
        Subreddit = self.Reddit.subreddit(Subreddit)
    
        if (SubCategory.lower() == "top"):  # Gets post from speceified category given by user
            TopPosts = Subreddit.top(limit=PostNumber)
        elif (SubCategory.lower() == "hot"):
            TopPosts = Subreddit.hot(limit=PostNumber)
        elif (SubCategory.lower() == "new"):
            TopPosts = Subreddit.new(limit=PostNumber)
        elif (SubCategory.lower() == "rising"):
            TopPosts = Subreddit.rising(limit=PostNumber)
          
        AllPosts = []  # Gets post from subreddit category 
        for Submission in TopPosts:
            AllPosts.append(Submission)
    
        Post = AllPosts[PostNumber - 1]
      
        Title = Post.title
        # If post title exceeds character limit, remove last 4 letters and add "...." 
        if (len(Title) > 256):  
            Title = Title[0:252] + "...."

        #  Getting post data to add to embed
        URL = Post.url 
        PostInfo = f"Post #{PostNumber} in {SubCategory} of r/{Subreddit}\nBy u/{Post.author}"
        UpRatio = f"Upvote Ratio: {str(round(Post.upvote_ratio * 100, 1))}%"
        Comments = f" & has {str(Post.num_comments)} comments"
        PostDate = "\nPosted on " + (datetime.fromtimestamp(Post.created_utc / 1000)).strftime('%Y-%m-%d at %I:%M %p')
      
        PostFlairs = "\nFlairs: None"
        if (Post.link_flair_text != None):  # If post has flairs
            PostFlairs = f"\nFlairs: {Post.link_flair_text}"
    
        Embed = discord.Embed(title=Title,
                              description=Post.selftext,
                              color=discord.Color.from_rgb(255, 16, 251))
    
        if (URL.endswith("jpg")):  # If post is an image
            Embed.set_image(url=URL)
    
        if "poll_data" in dir(Post):  # If post is a poll 
            Poll = Post.poll_data
            PollEnd = (datetime.fromtimestamp(Poll.voting_end_timestamp /1000)).strftime("%Y-%m-%d")
            PollData = f"Total Number of votes: {str(Poll.total_vote_count)}\nVoting end on: {PollEnd}"
            PollOptions = ""
          
            i = 0
            for option in Poll.options:  # Gets poll options to add to embed
                i += 1
                PollOptions += f"{i}- {option}  --->  {option.vote_count} votes\n"
              
            Embed.add_field(name="Poll Options", value=PollOptions, inline=False)  # Adds poll info to post
            Embed.add_field(name="Poll Data", value=PollData, inline=False)
    
        Embed.add_field(name=PostInfo,
                        value=UpRatio + Comments + PostDate + PostFlairs,
                        inline=False)  # Adds post info to embed
      
        Embed.add_field(name="Post URL", value=URL, inline=False)  # Adds post URL to embed
    
        Embed.set_thumbnail(url=self.Thumbnail)  # Adds thumbnail to embed
      
        Embed.set_footer(text="『Xrbot』", icon_url=self.Logo)  # Adds bot Logo to embed
      
        await ctx.send(embed=Embed)
    
    
    async def ViewUser(self, ctx):  # Shows info about a user
        User = ctx.message.content.lower().replace("x!reddit view ", "")
        # Checks if User exists
        try:
            self.Reddit.redditor(User).id
          
        except NotFound:  # Checks if user exists
            await ctx.send(f"User u/{User} does not exist")
            return
    
        Redditor = self.Reddit.redditor(User)
    
        Submissions = ""
        i = 1
        for submissions in Redditor.submissions.new(
                limit=10):  # Return title of last 10 posts
            Submissions += f"\n{str(i)}) {str(submissions.title)}\n"
            i += 1
    
        if (Submissions == ""):  # If redditor doesnt have any posts
            Submissions = "None"
    
        Karma = f"Post Karma: {str(Redditor.link_karma)}\nComment Karma: {str(Redditor.comment_karma)}"
      
        CreationTime = "Created on" + (datetime.fromtimestamp(Redditor.created_utc)).strftime("%Y-%m-%d")
    
        Embed = discord.Embed(title=Redditor.name,
                              description=CreationTime,
                              color=discord.Color.from_rgb(68, 255, 26)) 
      
        Embed.add_field(name="Most recent submissions:",
                        value=Submissions,
                        inline=False)
      
        Embed.add_field(name="Karma", 
                        value=Karma, 
                        inline=False)
      
        Embed.set_image(url=Redditor.icon_img)  # Adds profile picture embed
      
        Embed.set_thumbnail(url=self.Thumbnail)  # Adds bot Logo to embed
      
        Embed.set_footer(text="『Xrbot』", icon_url=self.Logo)  # Adds bot Logo to embed
      
        await ctx.send(embed=Embed)
    
    
    async def SubredditView(self, ctx):  # Shows info about a subreddit
        Subreddit = ctx.message.content.lower().replace("x!reddit sub ", "")
      
        # Checks if Subreddit exists
        try:
            self.Reddit.subreddits.search_by_name(Subreddit, exact=True)
          
        except NotFound:  # if Subreddit doesnt exist, returns 
            await ctx.send(f"Subreddit r/{Subreddit} does not exist")
            return
    
        Subreddit = self.Reddit.subreddit(Subreddit)  
        CreationTime = (datetime.fromtimestamp(Subreddit.created_utc)).strftime("%Y-%m-%d")
        MemberCount =  f"Subreddit members: {str(Subreddit.subscribers)}"
        SubredditInfo = f"{MemberCount} \nNSFW: {str(Subreddit.over18)}\nCreated on: {CreationTime}"
      
        # If post title exceeds character limit, remove last 4 letters and add "...."
        if (len(Subreddit.description) > 1024):
            SubredditDescription = Subreddit.description[0:1021] + "..."
        else:
            SubredditDescription = Subreddit.description
    
        Embed = discord.Embed(title=f"r/{Subreddit.display_name}",
                              description=Subreddit.public_description,
                              color=discord.Color.from_rgb(255, 137, 220))
      
        Embed.add_field(name="Subreddit info:",
                        value=SubredditInfo,
                        inline=False)
      
        Embed.add_field(name="Description:",
                        value=SubredditDescription,
                        inline=False)
      
        Embed.set_thumbnail(url=self.Thumbnail)  # Adds logo to embed
      
        Embed.set_footer(text="『Xrbot』", icon_url=self.Logo)  # Adds bot Logo to embed
      
        await ctx.send(embed=Embed)

