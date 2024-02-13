import disnake
from disnake.ext import commands

from client import client
from config.message import ban_bot, ban_top_roles, ban_user_is_blocked

class OnBan(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.has_permissions(ban_members=True)
    @commands.slash_command(name='ban', description='Заблокировать пользователя.')
    async def ban_command(self, inter: disnake.AppCmdInter, user: disnake.Member, reason: str):
        """
        Parameters
        ----------
        inter: None
        user: Укажите пользователя для блокировки
        times: Укажите время в формате <1-30><s/m/h/d>. Пример: 7d
        reason: Укажите причину блокировки
        """

        if user.bot:
            await inter.response.send_message(embed=disnake.Embed(description=ban_bot, color=0x2b2d31), ephemeral=True)
            return

        if user.top_role >= inter.author.top_role and inter.author != inter.guild.owner:
            await inter.response.send_message(embed=disnake.Embed(description=ban_top_roles, color=0x2b2d31), ephemeral=True)
            return

        await inter.response.defer()

        await user.ban(reason=reason)

        await inter.followup.send(embed=disnake.Embed(description=ban_user_is_blocked.format(inter.author.mention, user.mention, reason), color=0x2b2d31))

def setup(bot: commands.Bot):
    bot.add_cog(OnBan(client))
