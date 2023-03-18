import discord
from discord import app_commands, Interaction
from discord.ext import commands

class Testing(commands.Cog):
    """Testing commands cause idk what I'm doing lol."""

    def __init__(self, bot: commands.Bot):
        super().__init__
        self.bot = bot

    @app_commands.command()
    async def test(self, ctx: Interaction):
        await ctx.response.send_message("yep it works")

    @commands.command()
    async def test2(self, ctx: commands.Context):
        await ctx.send("yep it works")

async def setup(bot: commands.Bot):
    await bot.add_cog(Testing(bot))
    print("Successfully loaded module Testing.")