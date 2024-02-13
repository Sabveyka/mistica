import json
import disnake
from disnake.ext import commands

from client import client

class OnSlashCommandError(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            with open('config/discordPermissions.json', 'r', encoding='utf8') as discordPermissionsJSON:
                discordPermissions = json.load(discordPermissionsJSON)
            permission = discordPermissions[str(error.missing_permissions[0])]
            embed = disnake.Embed(description="**Вы должны иметь следующее право:**"
                                              f"\n- {permission}",
                                  color=0x303136)
            embed.set_author(name="У Вас недостаточно прав!",
                             icon_url=client.user.avatar.url)
            await inter.send(embed=embed)

        if isinstance(error, commands.NotOwner):
            embed = disnake.Embed(description="**Вы должны иметь следующее право:**"
                                              f"\n- Быть в числе разработчиков бота",
                                  color=0x303136)
            embed.set_author(name="У Вас недостаточно прав!",
                             icon_url=client.user.avatar.url)
            await inter.send(embed=embed)

        if isinstance(error, commands.BotMissingPermissions):
            with open('config/discordPermissions.json', 'r', encoding='utf8') as discordPermissionsJSON:
                discordPermissions = json.load(discordPermissionsJSON)
            permission = discordPermissions[str(error.missing_permissions[0])]
            embed = disnake.Embed(description="**Бот должен иметь следующее право:**"
                                              f"\n- {permission}",
                                  color=0x303136)
            embed.set_author(name="У бота недостаточно прав!",
                             icon_url=client.user.avatar.url)
            await inter.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(OnSlashCommandError(client))