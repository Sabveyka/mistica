import disnake
from disnake.ext import commands, tasks
from numdeclination import NumDeclination

client = commands.Bot(
    activity=disnake.Activity(type=disnake.ActivityType.playing, name="loading.."),
    case_insensitive=True,
    command_prefix=".",
    intents=disnake.Intents.all(),
    owner_id=577738174030413825,
    status=disnake.Status.dnd,
    strip_after_prefix=True,
    test_guilds=[1070397951542820884]
)

async def set_status():
    guild = client.get_guild(1070397951542820884)
    converted = NumDeclination().declinate(guild.member_count, ["участником", "участниками", "участниками"], type=4)

    await client.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.watching,
            name=f"за {converted.number} {converted.word}"),
        status=disnake.Status.dnd
    )

@tasks.loop(minutes=10)
async def statsServer():
    guild = client.get_guild(1070397951542820884)
    channel_users = guild.get_channel(1135536161071321220)
    channel_bot = guild.get_channel(1135536234651983966)

    bot_count = 0
    for i in guild.members:
        member = i.bot
        if member == True:
            bot_count += 1

    await channel_users.edit(name=f'Участников: {guild.member_count - bot_count}')
    await channel_bot.edit(name=f'Ботов: {bot_count}')
