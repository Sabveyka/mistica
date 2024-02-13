import disnake
from disnake.ext import commands

from client import client
from config.message import mute_bot, mute_top_roles, mute_exceeding_days, mute_user_is_muted

def time_converter(input_number: str):
    rep = {'в': 'd', 'р': 'h', 'ь': 'm', 'ы': 's',
           '!': '1', '@': '2', '"': '2', '#': '3', '№': '3',
           '$': '4', ';': '4', '%': '5', '^': '6', ':': '6',
           '&': '7', '?': '7', '*': '8', '(': '9', ')': '0'}

    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    res_input = replace_all(text=input_number, dic=rep)

    result_time = 0
    tmp = ''
    dict_to_sec = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    for w in res_input:
        if w.isdigit():
            tmp = tmp + w
        else:
            if w in dict_to_sec:
                result_time += int(tmp) * dict_to_sec[w]
            tmp = ''
    return result_time

class OnMute(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.has_permissions(moderate_members=True)
    @commands.slash_command(name='mute', description='Замутить пользователя.')
    async def mute_command(self, inter: disnake.AppCmdInter, user: disnake.Member, times: str, reason: str):
        """
        Parameters
        ----------
        inter: None
        user: Укажите пользователя, которого хотите замутить
        times: Укажите время в формате <1-30><s/m/h/d>. Пример: 7d
        reason: Укажите причину замутить
        """

        if user.bot:
            await inter.response.send_message(embed=disnake.Embed(description=mute_bot, color=0x2b2d31), ephemeral=True)
            return

        if user.top_role >= inter.author.top_role and inter.author != inter.guild.owner:
            await inter.response.send_message(embed=disnake.Embed(description=mute_top_roles, color=0x2b2d31), ephemeral=True)
            return

        result_time = time_converter(input_number=times)

        if result_time > 604800:
            await inter.response.send_message(embed=disnake.Embed(description=mute_exceeding_days, color=0x2b2d31), ephemeral=True)
            return

        await inter.response.defer()

        await user.timeout(reason=reason, duration=float(result_time))

        await inter.followup.send(embed=disnake.Embed(description=mute_user_is_muted.format(inter.author.mention, user.mention, times, reason), color=0x2b2d31))

def setup(bot: commands.Bot):
    bot.add_cog(OnMute(client))
