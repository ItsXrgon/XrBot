# Functions of the Reddit features of the bot
from datetime import datetime
import discord
from discord import Interaction
from discord.ext import commands
from discord.app_commands import command, describe, Choice, choices
import discord.ext.commands
import praw
from prawcore.exceptions import NotFound
from core.embed_builder import EmbedBuilder
import discord.ext


class RedditCommands(commands.Cog, name="reddit"):
    """Class for Reddit commands

    Args:
        commands (commands.Cog): The commands object
    """

    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id="YOUR CLIENT ID",
            client_secret="YOUR CLIENT SECRET",
            user_agent="redditdev scraper by u/Xron-_-",
            username="Xrbot-_-",
            password="YOUR PASSWORD",
            check_for_async=False,
        )
        self.thumbnail = "https://static.vecteezy.com/system/resources/thumbnails/008/385/732/small/reddit-social-media-icon-logo-abstract-symbol-illustration-free-vector.jpg"

    @command(
        name="top-post",
        description="Shows the top number of posts in a subreddit category",
    )
    @describe(
        category="The category of the feed (Top, New, etc.)",
        subreddit="The second number",
        post_number="The post number",
    )
    @choices(
        category=[
            Choice(name="top", value="top"),
            Choice(name="hot", value="hot"),
            Choice(name="new", value="new"),
            Choice(name="rising", value="rising"),
            Choice(name="controversial", value="controversial"),
            Choice(name="best", value="best"),
        ],
    )
    async def top_post(
        self,
        interaction: Interaction,
        category: Choice[str],
        subreddit: str,
        post_number: int = 0,
    ):
        """Shows the top number of posts in a subreddit category

        Args:
            interaction (Interaction): The interaction object
            category (Choice[str]): The category of the feed (Top, New, etc.)
            subreddit (str): The subreddit name
            post_number (int, optional): The post number. Defaults to 0.
        """

        # Checks if Subreddit exists
        try:
            self.reddit.subreddits.search_by_name(subreddit, exact=True)
        except NotFound:  # if Subreddit doesnt exist, returns
            await interaction.response.send_message(
                f"Subreddit r/{subreddit} does not exist"
            )
            return

        subreddit_obj = self.reddit.subreddit(subreddit)

        if category == "top":
            top_posts = subreddit_obj.top(limit=post_number)
        elif category == "hot":
            top_posts = subreddit_obj.hot(limit=post_number)
        elif category == "new":
            top_posts = subreddit_obj.new(limit=post_number)
        elif category == "rising":
            top_posts = subreddit_obj.rising(limit=post_number)
        elif category == "controversial":
            top_posts = subreddit_obj.controversial(limit=post_number)
        elif category == "best":
            top_posts = subreddit_obj.best(limit=post_number)

        posts = []  # Gets post from subreddit category
        for post in top_posts:
            posts.append(post)

        post = posts[post_number - 1]

        title = post.title
        # If post title exceeds character limit, remove last 4 letters and add "...."
        if len(title) > 256:
            title = title[0:252] + "...."

        #  Getting post data to add to embed
        url = post.url
        post_info = (
            f"Post #{post_number} in {category} of r/{subreddit}\nBy u/{post.author}"
        )
        up_ratio = f"Upvote Ratio: {str(round(post.upvote_ratio * 100, 1))}%"
        comments = f" & has {str(post.num_comments)} comments"
        post_date = "\nPosted on " + (
            datetime.fromtimestamp(post.created_utc / 1000)
        ).strftime("%Y-%m-%d at %I:%M %p")

        flairs = "\nFlairs: None"
        if post.link_flair_text is not None:  # If post has flairs
            flairs = f"\nFlairs: {post.link_flair_text}"

        embed_builder = EmbedBuilder(
            title=title,
            description=post.selftext,
            color=(255, 137, 220),
        )

        if url.endswith("jpg"):  # If post is an image
            embed_builder.set_image(url=url)

        if "poll_data" in dir(post):  # If post is a poll
            poll = post.poll_data
            poll_end = (
                datetime.fromtimestamp(poll.voting_end_timestamp / 1000)
            ).strftime("%Y-%m-%d")
            poll_data = f"Total Number of votes: {str(poll.total_vote_count)}\nVoting end on: {poll_end}"
            poll_options = ""

            i = 0
            for option in poll.options:  # Gets poll options to add to embed
                i += 1
                poll_options += f"{i}- {option}  --->  {option.vote_count} votes\n"

            embed_builder.add_field(
                name="Poll Options", value=poll_options, inline=False
            )  # Adds poll info to post
            embed_builder.add_field(name="Poll Data", value=poll_data, inline=False)

        embed_builder.add_field(
            name=post_info,
            value=up_ratio + comments + post_date + flairs,
            inline=False,
        )  # Adds post info to embed

        embed_builder.add_field(
            name="Post URL", value=url, inline=False
        )  # Adds post URL to embed

        embed_builder.set_thumbnail(url=self.thumbnail)  # Adds thumbnail to embed

        await interaction.response.send_message(embed=embed_builder.build())

    @command(
        name="view-user",
        description="Shows information about reddit a user",
    )
    @describe(user="The user name")
    async def view_user(self, interaction: Interaction, user: str):
        """Shows information about reddit a user

        Args:
            interaction (Interaction): The interaction object
            user (str): The user name
        """
        # Checks if User exists
        try:
            account = self.reddit.redditor(user)
            self.reddit.redditor(user).id
        except NotFound:  # Checks if user exists
            await interaction.response.send_message(f"User u/{user} does not exist")
            return

        posts = ""
        i = 1
        for submissions in account.submissions.new(
            limit=10
        ):  # Return title of last 10 posts
            posts += f"\n{str(i)}) {str(submissions.title)}\n"
            i += 1

        if posts == "":  # If redditor doesnt have any posts
            posts = "None"

        karma = f"Post Karma: {str(account.link_karma)}\nComment Karma: {str(account.comment_karma)}"

        creation_date = "Created on" + (
            datetime.fromtimestamp(account.created_utc)
        ).strftime("%Y-%m-%d")

        embed_builder = EmbedBuilder(
            title=account.name,
            description=creation_date,
            color=(68, 255, 26),
        )

        embed_builder.add_field(
            name="Most recent submissions:", value=posts, inline=False
        )
        embed_builder.add_field(name="Karma", value=karma, inline=False)
        embed_builder.set_image(url=account.icon_img)  # Adds profile picture embed
        embed_builder.set_thumbnail(url=self.thumbnail)  # Adds bot Logo to embed

        await interaction.response.send_message(embed=embed_builder.build())

    @command(
        name="sub",
        description="Shows information about a subreddit",
    )
    @describe(subreddit="The subreddit name")
    async def view_subreddit(self, interaction: Interaction, subreddit: str):
        # Checks if Subreddit exists
        try:
            self.reddit.subreddits.search_by_name(subreddit, exact=True)

        except NotFound:  # if Subreddit doesnt exist, returns
            await interaction.response.send_message(
                f"Subreddit r/{subreddit} does not exist"
            )
            return

        subreddit_obj = self.reddit.subreddit(subreddit)
        creation_date = (datetime.fromtimestamp(subreddit_obj.created_utc)).strftime(
            "%Y-%m-%d"
        )
        member_count = f"Subreddit members: {subreddit_obj.subscribers}"
        subreddit_info = f"{member_count} \nNSFW: {str(subreddit_obj.over18)}\nCreated on: {creation_date}"

        # If description exceeds character limit, remove last 4 letters and add "...."
        if len(subreddit_obj.description) > 1024:
            subreddit_description = subreddit_obj.description[0:1021] + "..."
        else:
            subreddit_description = subreddit_obj.description

        embed_builder = EmbedBuilder(
            title=f"r/{subreddit_obj.display_name}",
            description=subreddit_obj.public_description,
            color=(255, 137, 220),
        )

        embed_builder.add_field(
            name="Subreddit info:", value=subreddit_info, inline=False
        )
        embed_builder.add_field(
            name="Description:", value=subreddit_description, inline=False
        )
        embed_builder.set_thumbnail(url=self.thumbnail)

        await interaction.response.send_message(embed=embed_builder.build())


async def setup(client: discord.ext.commands.Bot) -> None:
    """Adds the RedditCommands cog to the bot

    Args:
        client (iscord.ext.commands.Bot): The client object
    """
    await client.add_cog(RedditCommands(client))
