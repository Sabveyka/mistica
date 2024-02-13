import disnake
from disnake.ext import commands

from client import client
from config.message import unban_user_is_blocked

class OnUnban(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.has_permissions(ban_members=True)
    @commands.slash_command(name='unban', description='Разблокировать пользователя.')
    async def unban_command(self, inter: disnake.AppCmdInter, user_id):
        """
        Parameters
        ----------
        inter: None
        user: Укажите пользователя для разблокировки
        """

        await inter.response.defer()

        await inter.guild.unban(user=client.fetch_user(int(user_id)))

        await inter.followup.send(embed=disnake.Embed(description=unban_user_is_blocked.format(inter.author.mention, f"<@{user_id}>"), color=0x2b2d31))

def setup(bot: commands.Bot):
    bot.add_cog(OnUnban(client))
