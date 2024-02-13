import disnake
from disnake.ext import commands

from client import client, set_status

class OnMemberRemove(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        await set_status()

def setup(bot: commands.Bot):
    bot.add_cog(OnMemberRemove(client))
