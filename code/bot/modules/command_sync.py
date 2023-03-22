import discord
from discord.ext import commands


class CommandSync(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__
        self.bot = bot
    
    @commands.command(name="globalsync", description="Sync all commands.")
    async def globalsync(self, ctx: commands.Context):
        await self.bot.tree.sync()
        await ctx.reply("Commands synced globally!")
        
    @commands.command(name="globalclear", description="Clear all commands.")
    async def globalclear(self, ctx: commands.Context):
        print("Clearing all commands globally.")
        await self.bot.tree.clear_commands()
        await self.bot.tree.sync()
        await ctx.reply("Commands cleared globally!")

    @commands.command(name="localsync", description="Sync all commands in the current guild.")
    async def localsync(self, ctx: commands.Context):
        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.reply("Commands synced locally!")

    @commands.command(name="localclear", description="Clear all commands in the current guild.")
    async def localclear(self, ctx: commands.Context):
        self.bot.tree.clear_commands(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.reply("Commands cleared locally!")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(CommandSync(bot))