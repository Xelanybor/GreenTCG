import os
from dotenv import load_dotenv
import discord
from discord import Intents
from discord.ext import commands
import asyncio



# Debug initialization
# ---------------------------------------------------------------------------------
load_dotenv()
try:
    if os.getenv("DEBUG").lower() == "true":
        DEBUG = True
    else:
        DEBUG = False
except:
    DEBUG = False
    
# Discord bot initialization
# ---------------------------------------------------------------------------------
# Load variables from the .env
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_PREFIX = os.getenv("PREFIX")
# Don't need this just yet but will make adding special intents later easier
intents = Intents.default()
intents.members = False

# Extend discord bot class
class Bot(commands.Bot):
    """
    Custom bot for the Green TCG.
    """
    
    def __init__(self):
        intents = discord.Intents.default()
        # intents.message_content = True
        super().__init__(
            command_prefix=DISCORD_PREFIX,
            intents=intents,
            case_insensitive=True,
            activity=discord.Game(name="Green TCG!"),
            status=discord.Status.online
            )
        # print(f"Created bot with prefix {DISCORD_PREFIX}")

# Create discord bot
bot = Bot()

async def main():

    # Load cogs
    for filename in os.listdir("src/modules"):
        if filename[-3:] == ".py" and filename != "__init__.py" and filename != "Testing.py":
            try:
                if DEBUG:
                    print(f"Attempting to load module \"{filename}\"...")
                await bot.load_extension(f"modules.{filename[:-3]}")
                if DEBUG:
                    print(f"Successfully loaded module \"{filename}\".")
            except Exception as e:
                print(f"Couldn't load module \"{filename}\": {e}")

    if DEBUG:
        print("Loading Test module...")
        try:
            await bot.load_extension("modules.Testing")
            print("Done")
        except Exception as e:
                print(f"Couldn't load module \"Testing\": {e}")

    # Bot startup
    # ---------------------------------------------------------------------------------

    @bot.event
    async def on_ready():
        print(f'Logged into Discord as {bot.user}.')

    print("Starting Green TCG Bot...")
    async with bot:
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())