import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, NoEntryPointError
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_DEV_ID = os.getenv("DISCORD_DEV_ID")

class NotDevError(commands.CheckFailure):
    """Error that is raised when someone who isn't a dev tries to use a dev-only command."""
    pass

def isDev():
    """Check to lock a command for only devs."""
    async def wrapper(ctx):
            if ctx.author.id == int(DISCORD_DEV_ID):
                return True
            else:
                raise NotDevError("You don't have permission to use this command.")
    return commands.check(wrapper)

class Cogs(commands.Cog):
    "Loads, unloads, and reloads command cogs."

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @isDev()
    async def load(self, ctx: commands.Context, cog: str):
        "Load a given cog."
        try:
            await self.bot.load_extension("modules." + cog)
            await ctx.send(f"Successfully loaded cog `{cog}`.")
        except ExtensionNotFound:
            await ctx.send(f"Cog `{cog}` was unable to be found!")
        except ExtensionAlreadyLoaded:
            await ctx.send(f"Cog `{cog}` is already loaded!")
        except NoEntryPointError or ExtensionFailed as e:
            await ctx.send(f"Unable to load cog: {e}")

    @commands.command(hidden=True)
    @isDev()
    async def unload(self, ctx: commands.Context, cog: str):
        "Unload a given cog."
        try:
            await self.bot.unload_extension("modules." + cog)
            await ctx.send(f"Successfully unloaded cog `{cog}`.")
        except ExtensionNotFound:
            await ctx.send(f"Cog `{cog}` was unable to be found!")
        except ExtensionNotLoaded:
            await ctx.send(f"Cog `{cog}` is already unloaded!")

    @commands.command(hidden=True)
    @isDev()
    async def reload(self, ctx: commands.Context, cog: str):
        "Reload a given cog."
        try:
            await self.bot.reload_extension("modules." + cog)
            await ctx.send(f"Successfully reloaded cog `{cog}`")
        except ExtensionNotFound:
            await ctx.send(f"Cog `{cog}` was unable to be found!")
        except ExtensionNotLoaded:
            await ctx.send(f"Cog `{cog}` must first be loaded!")

    # Ignore dev errors
    @load.error
    @unload.error
    @reload.error
    async def dev_error(self, ctx, error):
        if isinstance(error, NotDevError):
            await ctx.send(f"`{error}`")
        else:
            print(error)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Cogs(bot))