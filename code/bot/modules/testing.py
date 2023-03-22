import discord
from discord import app_commands, Interaction, ui
from discord.ext import commands

class Testing(commands.Cog):
    """Testing commands cause idk what I'm doing lol."""

    def __init__(self, bot: commands.Bot):
        super().__init__
        self.bot = bot

    @app_commands.command()
    async def test(self, ctx: Interaction):
        # await ctx.response.autocomplete([app_commands.Choice(name="Option A", value="A"), app_commands.Choice(name="Option B", value="B")])

        # class test_modal(ui.Modal, title="Test"):
        #     name = ui.TextInput(label='Name')
        #     answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

        #     async def on_submit(self, interaction: discord.Interaction):
        #         await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)

        # modal = test_modal()

        # await ctx.response.send_modal(modal)
        await ctx.response.send_message("yep it works")

    @commands.command()
    async def test2(self, ctx: commands.Context):
        await ctx.send("yep it works")
    
    @test.error
    async def print_errors(self, ctx, error):
        print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(Testing(bot))
    print("Successfully loaded module Testing.")

def test():
    print("bruh moment")