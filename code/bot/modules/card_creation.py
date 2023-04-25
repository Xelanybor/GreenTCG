import asyncio
import discord
from discord import app_commands, Interaction
from discord.ext import commands
import os
import typing

from modules.helpers import embeds, tcgui, card_creator

class CardCreation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="create-card")
    async def create_card(self, interaction: Interaction,
                          card_type: typing.Literal['Flairwarrior', 'Event', 'Role'],
                          card_color: typing.Literal['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Void'],
                          image_url: str
                          ):
        
        async def modal_callback(form, new_interaction: Interaction):
            await new_interaction.response.send_message("<a:discordIsTyping:1005500222899765308> Generating card...")
            print([
                str(form.card_name),
                str(form.card_type),
                str(form.card_color),
                str(image_url),
                str(form.desc1),
                str(form.desc2),
                str(form.atk),
                str(form.hp)
            ])
            img_file = card_creator.create_card_image(
                card_name=str(form.card_name),
                card_type=str(form.card_type),
                card_color=str(form.card_color),
                image_url=str(image_url),
                desc1=str(form.desc1),
                desc2=str(form.desc2),
                atk=int(str(form.atk)),
                hp=int(str(form.hp))
            )
            f = open(file=img_file, mode="rb")
            msg = await new_interaction.original_response()
            # await msg.edit(content='', attachments=discord.File(f))
            await msg.add_files(discord.File(f))
            await msg.edit(content="")
            f.close()
            os.remove(img_file)

        if card_type == "Flairwarrior":
            modal = tcgui.CreateFlairwarrior(card_color, modal_callback)
        elif card_type == "Event":
            modal = tcgui.CreateEvent(card_color, modal_callback)
        elif card_type == "Role":
            modal = tcgui.CreateRole(card_color, modal_callback)
        else:
            await interaction.response.send_message("An error occured while creating your card.", ephemeral=True)
            return

        await interaction.response.send_modal(modal)
    
    @create_card.error
    async def print_errors(self, interaction, error):
        print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(CardCreation(bot))