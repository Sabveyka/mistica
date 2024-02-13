import disnake
from disnake.ext import commands

from client import client, set_status
from config.config import GREETINGS_CHANNEL, GREETINGS_ROLE

class OnMemberJoin(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        await member.add_roles(
            member.guild.get_role(GREETINGS_ROLE),
            reason=f'New member. {member.guild.member_count}'
        )

        embed = disnake.Embed(
            description="Ознакомься с нашими [правилами](https://discord.com/channels/1070397951542820884/1126482285710028810) и не нарушай их!\n\nНадеюсь тебе понравится у нас, удачи! :heart:",
            color=0x2b2d31
        )

        await member.guild.get_channel(GREETINGS_CHANNEL).send(f"# Добро пожаловать на сервер, {member.mention}!", embed=embed)
        await set_status()

def setup(bot: commands.Bot):
    bot.add_cog(OnMemberJoin(client))
