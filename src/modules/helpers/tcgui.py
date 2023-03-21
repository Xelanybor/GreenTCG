"""Contains discord.ui views to let the user interact with the bot ui."""

import discord
from discord import ui

from modules.helpers import embeds

class OpenChallenge(ui.View):

    def __init__(self, *, challenger: discord.User, accept_callback, cancel_callback):
        super().__init__()
        self.challenger = challenger
        self.accept_callback = accept_callback
        self.cancel_callback = cancel_callback

    @ui.button(label='Accept', style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.challenger.id:
            await interaction.response.send_message(f"You can't accept your own challenge!", ephemeral=True)
            return
        await interaction.response.defer()
        await self.accept_callback(interaction)
        self.stop()

    @ui.button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.challenger.id:
            await interaction.response.send_message(f"I'm sorry, only {self.challenger.display_name} can cancel to this challenge!", ephemeral=True)
            return
        await interaction.response.defer()
        await self.cancel_callback(interaction)
        self.stop()

class ClosedChallenge(ui.View):

    def __init__(self, *, challenger: discord.User, opponent: discord.User, accept_callback, decline_callback, cancel_callback):
        super().__init__()
        self.challenger = challenger
        self.opponent = opponent
        self.accept_callback = accept_callback
        self.decline_callback = decline_callback
        self.cancel_callback = cancel_callback

    @ui.button(label='Accept', style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.opponent.id:
            await interaction.response.send_message(f"I'm sorry, only {self.opponent.display_name} can respond to this challenge!", ephemeral=True)
            return
        await interaction.response.defer()
        await self.accept_callback(interaction)
        self.stop()

    @ui.button(label='Decline', style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.opponent.id:
            await interaction.response.send_message(f"I'm sorry, only {self.opponent.display_name} can respond to this challenge!", ephemeral=True)
            return
        await interaction.response.defer()
        await self.decline_callback(interaction)
        self.stop()

    @ui.button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.challenger.id:
            await interaction.response.send_message(f"I'm sorry, only {self.challenger.display_name} can cancel to this challenge!", ephemeral=True)
            return
        await interaction.response.defer()
        await self.cancel_callback(interaction)
        self.stop()