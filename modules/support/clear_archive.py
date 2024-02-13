import json
import sqlite3

import disnake
from disnake.ext import commands

from client import client
from config.message import arch_deleted_archive_ticket, arch_nothing_to_delete


async def cleansing(category: disnake.CategoryChannel, administrator: disnake.Member):
    for channel in category.text_channels:
        await channel.delete(reason=f"Clearing the archive by the {administrator} administrator")


class OnClearArchive(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name='clear_archive')
    async def clear_archive_command(self, inter: disnake.AppCmdInter):
        category = inter.guild.get_channel(1135549619238084809)

        if len(category.channels) == 0:
            await inter.send(embed=disnake.Embed(description=arch_nothing_to_delete, color=0x2b2d31))
            return


        await inter.send(embed=disnake.Embed(description=arch_deleted_archive_ticket.format(len(category.channels)), color=0x2b2d31))
        await cleansing(category=category, administrator=inter.author.name)


def setup(bot: commands.Bot):
    bot.add_cog(OnClearArchive(client))
