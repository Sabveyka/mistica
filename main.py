import os
import sqlite3
from disnake.ext import tasks
from dotenv import load_dotenv

from config.config import MODULES, MAIN_CHANNEL, MAIN_MESSAGE
from config.message import bot_on_ready
from modules.recruitment import SelectStaffRoleView, Solution
from modules.support.button import OpenTicketButton, CloseTicketButton, ReopenOrHideTicketButton
from client import client, set_status, statsServer


load_dotenv()

@tasks.loop(hours=3)
async def __updateButtonInfo__():
    db = sqlite3.connect('db/server.db')
    cursor = db.cursor()

    try:
        channel = client.get_channel(MAIN_CHANNEL)
        message = await channel.fetch_message(MAIN_MESSAGE)
        await message.edit(view=OpenTicketButton())
    except Exception as e:
        print(f"[OpenTicketButton] {e}")

    try:
        cursor.execute("SELECT * FROM ticket")

        for channel_id in cursor.fetchall():
            status_button = cursor.execute("SELECT button_status FROM ticket WHERE channel_id=?", (channel_id[0], )).fetchone()[0]
            if status_button == "close":
                get_channel = client.get_channel(channel_id[0])
                message = await get_channel.fetch_message(cursor.execute("SELECT message_id FROM ticket WHERE channel_id=?", (channel_id[0], )).fetchone()[0])
                await message.edit(view=CloseTicketButton())
            if status_button == "reopen":
                get_channel = client.get_channel(channel_id[0])
                message = await get_channel.fetch_message(cursor.execute("SELECT message_id FROM ticket WHERE channel_id=?", (channel_id[0], )).fetchone()[0])
                await message.edit(view=ReopenOrHideTicketButton())
    except Exception as e:
        print(f"[InTicketButton] {e}")

@tasks.loop(hours=3)
async def __updateButtonInfoFake_():
    db = sqlite3.connect('db/server.db')
    cursor = db.cursor()

    try:
        channel = client.get_channel(1123253477586514031)
        message = await channel.fetch_message(1123256426584866866)
        await message.edit(view=SelectStaffRoleView())
    except Exception as e:
        print(f"[SelectStaffRoleView_error] {e}")

    try:
        cursor.execute("SELECT * FROM recruitment")

        guild = client.get_guild(1002204164924903574)
        for channel_id in cursor.fetchall():
            channel = guild.get_channel(int(channel_id[0]))
            message = await channel.fetch_message(cursor.execute("SELECT message_id FROM recruitment WHERE channel_id=?", (channel_id[0], )).fetchone()[0])
            await message.edit(view=Solution())
    except Exception as e:
        print(f"[я хуй знает как тебя назвать] {e}")

    db.close()

@client.event
async def on_ready():
    if not __updateButtonInfo__.is_running():
        __updateButtonInfo__.start()
    if not statsServer.is_running():
        statsServer.start()
    await set_status()
    print(bot_on_ready.format(client.user.name, client.user, client.user.id))


if __name__ == "__main__":

    for extension in MODULES:
        module: str = f"modules.{extension}"
        try:
            client.load_extension(module)
        except Exception as error_connection:
            print(error_connection)

    db = sqlite3.connect('db/server.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS bans (
                   user_id INT,
                   moderator_id INT,
                   unix_time INT,
                   reason TEXT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS muted (
                   user_id INT,
                   moderator_id INT,
                   unix_time INT,
                   reason TEXT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS recruitment (
                   channel_id INT,
                   owner_id INT,
                   message_id INT,
                   title TEXT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS ticket (
                   channel_id INT,
                   owner_id INT,
                   button_status TEXT,
                   message_id INT
    )""")

    db.commit()
    db.close()

    client.run(os.getenv('TOKEN'))