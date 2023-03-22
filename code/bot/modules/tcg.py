import asyncio
import discord
from discord import app_commands, Interaction
from discord.ext import commands

from modules.helpers import embeds, tcgui

class TCG(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def challenge(self, interaction: Interaction, opponent: discord.User = None):

        challenger = interaction.user

        opponent_responded = asyncio.Event()

        if opponent:

            async def accept(new_interaction: Interaction):
                nonlocal interaction
                interaction = new_interaction
                opponent_responded.set()

            async def decline(new_interaction: Interaction):
                nonlocal opponent
                embed = embeds.decline_challenge(opponent=opponent)
                await new_interaction.edit_original_response(embed=embed, view=None)
                opponent = None
                opponent_responded.set()

            async def cancel(new_interaction: Interaction):
                nonlocal opponent
                embed = embeds.cancel_challenge(challenger=challenger)
                await new_interaction.edit_original_response(content="", embed=embed, view=None)
                opponent = None
                opponent_responded.set()

            view = tcgui.ClosedChallenge(challenger=challenger, opponent=opponent, accept_callback=accept, decline_callback=decline, cancel_callback=cancel)
            embed = embeds.closed_challenge(challenger=challenger, opponent=opponent)
            await interaction.response.send_message(content=opponent.mention, embed=embed, view=view)


        else:
        
            async def accept(new_interaction: Interaction):
                nonlocal interaction
                interaction = new_interaction
                nonlocal opponent
                opponent = new_interaction.user
                opponent_responded.set()
            
            async def cancel(new_interaction: Interaction):
                nonlocal opponent
                embed = embeds.cancel_challenge(challenger=challenger)
                await new_interaction.edit_original_response(embed=embed, view=None)
                opponent = None
                opponent_responded.set()

            view = tcgui.OpenChallenge(challenger=challenger, accept_callback=accept, cancel_callback=cancel)
            embed = embeds.open_challenge(challenger=challenger)
            await interaction.response.send_message(embed=embed, view=view)


        await opponent_responded.wait()
        if not opponent:
            return


        e = discord.Embed(title=f"{challenger.display_name} vs {opponent.display_name}")
        e.color = discord.Colour.green()
        
        e.set_image(url="https://assets.reedpopcdn.com/hearthstone-is-coming-to-android-tablets-before-end-of-year-1413918068236.jpg/BROK/thumbnail/1600x900/quality/100/hearthstone-is-coming-to-android-tablets-before-end-of-year-1413918068236.jpg")
        await interaction.edit_original_response(
            content=f"{challenger.mention} vs {opponent.mention} - Round 1",
            embed=e,
            view=None
            )
        
        original_response = await interaction.original_response()
        thread = await original_response.create_thread(name=f"{challenger.display_name} vs {opponent.display_name} - GTCG The Game™",
                                                        #  type=discord.ChannelType.public_thread,
                                                         reason="Green TCG"
                                                         )
        
        # await thread.send(f"{challenger.mention} has challenged {opponent.mention} to a game of TCG!")
        # print(f'Starter message: "{thread.starter_message.content}"')

    
    @challenge.error
    async def print_errors(self, interaction, error):
        print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(TCG(bot))