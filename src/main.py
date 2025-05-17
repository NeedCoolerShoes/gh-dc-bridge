import discord
import logging
import logging.handlers
import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv(dotenv_path=".env")

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    filename="discord.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

with open(os.getenv("GITHUB_PRIVATE_KEY_LOCATION"), "r") as secret:
    private_key = secret.read()

client = discord.Client(intents=intents)
app = Auth.AppAuth(app_id=os.getenv("GITHUB_APP_ID"), private_key=private_key).get_installation_auth(os.getenv("GITHUB_INSTALLATION_ID"))
gh = Github(auth=app)

@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel == discord.Thread:
        return
        # logger.info(f"Message in thread: {message.content} (ID: {message.id})")
        # if message.content.startswith("!close"):
        #     await message.channel.send("Closing thread...")
        #     await message.channel.edit(archived=True)
        #     logger.info(f"Thread closed: {message.channel.name} (ID: {message.channel.id})")
        #     return


@client.event
async def on_thread_create(thread):
    logger.info(f"Thread created: {thread.name} (ID: {thread.id})")
    # await thread.send(f"Thread created: {thread.name} (ID: {thread.id})")
    # await thread.send(f"Thread created by: {thread.owner} (ID: {thread.owner.id})")
    if thread.parent_id == os.getenv("DISCORD_FEATURE_REQUEST_CHANNEL_ID"):
        await thread.send("This is a feature request thread.")
        await thread.send("Creating a feature request issue on GitHub")
        logger.info("Creating feature request issue on GitHub")
        issue = gh.get_repo(os.getenv("GITHUB_REPO")).create_issue(title=f"[FEATURE] {thread.name}", body=f"Author: {thread.owner.nick}\n=================\n{thread.starter_message.content}")
        await thread.send(f"Feature request issue created on GitHub\n[Click me!]({issue.url})")
        logger.info(f"Feature request issue created on GitHub. URL: {issue.url}")
    elif thread.parent_id == os.getenv("DISCORD_BUG_REPORT_CHANNEL_ID"):
        await thread.send("This is a bug report thread.")
        await thread.send("Creating a bug report issue on GitHub")
        logger.info("Creating feature request issue on GitHub")
        issue = gh.get_repo(os.getenv("GITHUB_REPO")).create_issue(title=f"[BUG] {thread.name}", body=f"Author: {thread.owner.nick}\n=================\n{thread.starter_message.content}")
        await thread.send(f"Feature bug report created on GitHub\n[Click me!]({issue.url})")
        logger.info(f"Feature request issue created on GitHub. URL: {issue.url}")
    else:
        logger.info("Thread irrelevant to feature request or bug report")

client.run(os.getenv("DISCORD_TOKEN"))