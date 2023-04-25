import asyncio
import discord
from discord import app_commands, Interaction
from discord.ext import commands

from modules.helpers import embeds, tcgui, match_manager

class LobbyManagement(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.MM = match_manager.MatchManager()
    
    @app_commands.command()
    async def lobbies(self, interaction: Interaction):
        available, busy = self.MM.get_lobbies()
        e = embeds.lobbies(available_lobbies=available, busy_lobbies=busy)
        await interaction.response.send_message(embed=e)

    @app_commands.command()
    async def challenge(self, interaction: Interaction, opponent: discord.User = None):

        if not self.MM.lobbies_available():
            await interaction.response.send_message("I'm sorry, there are currently no available lobbies. Use the `/lobbies` command to see what lobbies are currently in use.", ephemeral=True)
            return

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
        
        # not thread-safe but that's assuming there are going to be more than two people wanting to play at any one time lmao
        # yeah right
        lobby_code = self.MM.start_match()

        e = embeds.match_in_progress(challenger=challenger, opponent=opponent)

        async def end_match(new_interaction: Interaction):
            embed = embeds.match_ended(challenger=challenger, opponent=opponent)
            self.MM.end_match(lobby_code)
            await new_interaction.edit_original_response(embed=embed, view=None)

        view = tcgui.OngoingMatch(players=(challenger, opponent), lobby_code=lobby_code, end_match_callback=end_match)
        
        await interaction.edit_original_response(
            content=f"{challenger.mention} vs {opponent.mention}",
            embed=e,
            view=view
            )
        
        original_response = await interaction.original_response()
        thread = await original_response.create_thread(name=f"{challenger.display_name} vs {opponent.display_name} - GTCG The Game™",
                                                        #  type=discord.ChannelType.public_thread,
                                                         reason="Green TCG"
                                                         )
        
        # await thread.send(f"{challenger.mention} has challenged {opponent.mention} to a game of TCG!")
        # print(f'Starter message: "{thread.starter_message.content}"')

    @lobbies.error
    @challenge.error
    async def print_errors(self, interaction, error):
        print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(LobbyManagement(bot))