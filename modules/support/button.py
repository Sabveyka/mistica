import sqlite3
import disnake

from client import client
from config.config import SUPPORT_ROLE, OPEN_TICKET_CATEGORY, CLOSE_TICKET_CATEGORY, HIDE_TICKET_CATEGORY
from config.message import support_only_two_channel, support_ticket_created

class OpenTicketButton(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @disnake.ui.button(label="Открыть тикет", style=disnake.ButtonStyle.green, emoji="📨")
    async def open_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):

        await inter.response.defer()

        db = sqlite3.connect('db/server.db')
        cursor = db.cursor()

        cursor.execute("SELECT * FROM ticket")
        for ticket_id in cursor.fetchall():
            if cursor.execute("SELECT channel_id FROM ticket WHERE owner_id=?", (inter.author.id, )).fetchone():
                channel = client.get_channel(int(ticket_id[0]))
                await inter.followup.send(embed=disnake.Embed(description=support_only_two_channel.format(channel.mention), color=0xFF0000), ephemeral=True)
                return

        support_role = inter.guild.get_role(SUPPORT_ROLE)
        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            inter.author: disnake.PermissionOverwrite(view_channel=True,
                                                      send_messages=True,
                                                      embed_links=True,
                                                      attach_files=True,
                                                      read_message_history=True,
                                                      use_application_commands=True),
            support_role: disnake.PermissionOverwrite(view_channel=True,
                                                     send_messages=True,
                                                     embed_links=True,
                                                     attach_files=True,
                                                     read_message_history=True,
                                                     manage_messages=True,
                                                     use_application_commands=True)
        }

        ticket_channel = await inter.guild.create_text_channel(
            f"ticket-{inter.author.name}",
            category=inter.guild.get_channel(OPEN_TICKET_CATEGORY),
            overwrites=overwrites
        )

        embed = disnake.Embed(
            description=f"Здравствуйте, {inter.author.mention}!"
                        f"\n\nВы открыли тикет. Оставьте своё обращение здесь."
                        f"\nРассмотрением обращений занимаются люди с ролью {support_role.mention}."
                        f"\nВы можете посмотреть кто из сотрудников сейчас онлайн с помощью взаимодействия \"Сотрудники онлайн\"."
                        f"\n\nПомните, что сотрудники технической поддержки тоже люди. Ответ поступит в течении *24-ёх часов*.",
            color=0xFF0000
        )
        embed.set_author(name=inter.guild.name, icon_url=client.user.avatar.url)

        message = await ticket_channel.send("{support_role.mention} -> {inter.author.mention}", embed=embed, view=CloseTicketButton())
        await message.pin()

        cursor.execute("INSERT INTO ticket VALUES (?, ?, ?, ?)", (ticket_channel.id, inter.author.id, 'close', message.id))
        db.commit()
        db.close()

        await inter.followup.send(embed=disnake.Embed(description=support_ticket_created.format(ticket_channel.mention), color=0xFF0000), ephemeral=True)


class CloseTicketButton(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @disnake.ui.button(label="Закрыть тикет", style=disnake.ButtonStyle.red, emoji="⚠️")
    async def closeTicketButton(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):

        await inter.response.defer()

        await inter.message.edit(view=None)

        db = sqlite3.connect('db/server.db')
        cursor = db.cursor()

        support_role = inter.guild.get_role(SUPPORT_ROLE)
        owner_ticket = inter.guild.get_member(cursor.execute("SELECT owner_id FROM ticket WHERE channel_id=?", (inter.channel.id, )).fetchone()[0])

        permission_owner = inter.channel.overwrites_for(owner_ticket)
        permission_owner.send_messages = False
        permission_owner.embed_links = False
        permission_owner.attach_files= False

        permission_support = inter.channel.overwrites_for(support_role)
        permission_support.send_messages = False
        permission_support.embed_links = False
        permission_support.attach_files = False
        permission_support.manage_messages = False


        embed = disnake.Embed(
            description=f"Уважаемый, {owner_ticket.mention}!"
                        f"\n\nВаш тикет был закрыт. Вы можете управлять им в случае необходимости.",
            color=0xFF0000
        )
        embed.add_field(name="📨 Переоткрыть тикет", value=f"Переоткроет обращение для Вас и {support_role.mention}.\n└_Использовать при новом обращении!_", inline=True)
        embed.add_field(name="🗑️ Скрыть тикет", value=f"Скроет обращение и удалит его из базы-данных.\n└_Вы потеряете доступ к тикету!_", inline=True)
        embed.add_field(name="💼 Сотрудники онлайн", value=f"Просмотр онлайн сотрудников.\n└_Сотрудники, которых Вы можете упомянуть!_", inline=True)
        embed.set_author(name=inter.guild.name, icon_url=client.user.avatar.url)
        embed.set_footer(text=f'{inter.author.name} ({inter.author}) закрыл тикет.', icon_url=inter.author.avatar.url if inter.author.avatar != None else inter.guild.icon.url if inter.guild.icon != None else None)

        message = await inter.followup.send(embed=embed, view=ReopenOrHideTicketButton())

        await inter.message.channel.set_permissions(target=support_role, overwrite=permission_support)
        await inter.message.channel.set_permissions(target=owner_ticket, overwrite=permission_owner)

        await inter.channel.edit(category=inter.guild.get_channel(CLOSE_TICKET_CATEGORY))

        cursor.execute("UPDATE ticket SET button_status=? WHERE channel_id=?", ("reopen", inter.channel.id))
        cursor.execute("UPDATE ticket SET message_id=? WHERE channel_id=?", (message.id, inter.channel.id))
        db.commit()
        db.close()

    @disnake.ui.button(label="Сотрудники онлайн", style=disnake.ButtonStyle.gray, emoji="💼")
    async def staff_online_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):

        await inter.response.defer()

        staff = ""
        num = 0

        for user in inter.guild.get_role(SUPPORT_ROLE).members:
            if str(user.status) == 'online' or str(user.status) == 'idle' or str(user.status) == 'dnd':
                num += 1
                staff += f"`{num}.` {user.mention}\n"

        if num == 0:
            title = "Сотрудников онлайн: Нет"
        else:
            title = f"Сотрудников онлайн: {num}"

        embed = disnake.Embed(
            title=title,
            description=staff,
            color=0xFF0000
            )
        embed.set_author(name=inter.guild.name,
                         icon_url=client.user.avatar.url)
        await inter.followup.send(embed=embed, ephemeral=True)


class ReopenOrHideTicketButton(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @disnake.ui.button(label="Переоткрыть тикет", style=disnake.ButtonStyle.red, emoji="📨")
    async def reopen_ticket(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):

        await inter.response.defer()

        await inter.message.edit(view=None)

        db = sqlite3.connect('db/server.db')
        cursor = db.cursor()

        support_role = inter.guild.get_role(SUPPORT_ROLE)
        owner_ticket = inter.guild.get_member(cursor.execute("SELECT owner_id FROM ticket WHERE channel_id=?", (inter.channel.id, )).fetchone()[0])

        permission_owner = inter.channel.overwrites_for(owner_ticket)
        permission_owner.send_messages = True
        permission_owner.embed_links = True
        permission_owner.attach_files= True

        permission_support = inter.channel.overwrites_for(support_role)
        permission_support.send_messages = True
        permission_support.embed_links = True
        permission_support.attach_files = True
        permission_support.manage_messages = True


        embed = disnake.Embed(
            description=f"Тикет был переоткрыт. Оставьте своё новое обращение здесь."
                        f"\n\nПомните, что сотрудники технической поддержки тоже люди. Ответ поступит в течении *24-ёх часов*.",
            color=0xFF0000
        )
        embed.set_author(name=inter.guild.name, icon_url=client.user.avatar.url)
        embed.set_footer(text=f'{inter.author.name} ({inter.author}) переоткрыл тикет.', icon_url=inter.author.avatar.url if inter.author.avatar != None else inter.guild.icon.url if inter.guild.icon != None else None)

        message = await inter.followup.send(embed=embed, view=CloseTicketButton())

        await inter.message.channel.set_permissions(target=support_role, overwrite=permission_support)
        await inter.message.channel.set_permissions(target=owner_ticket, overwrite=permission_owner)

        await inter.channel.edit(category=inter.guild.get_channel(OPEN_TICKET_CATEGORY))

        cursor.execute("UPDATE ticket SET button_status=? WHERE channel_id=?", ("close", inter.channel.id))
        cursor.execute("UPDATE ticket SET message_id=? WHERE channel_id=?", (message.id, inter.channel.id))
        db.commit()
        db.close()

    @disnake.ui.button(label="Скрыть тикет", style=disnake.ButtonStyle.green, emoji="🗑️")
    async def hide_ticket(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):

        await inter.response.defer()

        await inter.message.edit(view=None)

        db = sqlite3.connect('db/server.db')
        cursor = db.cursor()

        support_role = inter.guild.get_role(SUPPORT_ROLE)
        owner_ticket = inter.guild.get_member(cursor.execute("SELECT owner_id FROM ticket WHERE channel_id=?", (inter.channel.id, )).fetchone()[0])

        permission_owner = inter.channel.overwrites_for(owner_ticket)
        permission_owner.view_channel = False
        permission_owner.send_messages = False
        permission_owner.embed_links = False
        permission_owner.attach_files= False
        permission_owner.read_message_history = False
        permission_owner.use_application_commands = False

        permission_support = inter.channel.overwrites_for(support_role)
        permission_support.send_messages = False
        permission_support.embed_links = False
        permission_support.attach_files= False
        permission_support.manage_messages = False
        permission_support.use_application_commands = False

        embed = disnake.Embed(color=0xFF0000)
        embed.set_author(name=inter.guild.name, icon_url=client.user.avatar.url)
        embed.set_footer(text=f'{inter.author.name} ({inter.author}) скрыл тикет.', icon_url=inter.author.avatar.url if inter.author.avatar != None else inter.guild.icon.url if inter.guild.icon != None else None)

        await inter.followup.send(embed=embed)

        await inter.message.channel.set_permissions(target=support_role, overwrite=permission_support)
        await inter.message.channel.set_permissions(target=owner_ticket, overwrite=permission_owner)


        await inter.channel.edit(category=inter.guild.get_channel(HIDE_TICKET_CATEGORY))


        cursor.execute("DELETE FROM ticket WHERE channel_id=?", (inter.channel.id, ))
        db.commit()
        db.close()