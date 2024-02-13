#
# Конфигурация отправляемых сообщений
#

# EMOTES

yes = ":white_check_mark: "
no = ":x: "

# GLOBAL

bot_on_ready = '{} [({}) ({})] готов к работе.'
dont_permission = no + 'У Вас недостаточно прав.'

# BAN & UNBAN

ban_bot = 'Я не могу заблокировать или разблокировать ботов.'
ban_top_roles = 'У Вас нет прав заблокировать этого пользователя.'
ban_user_is_blocked = '{} заблокировал {} по причине "{}".'

unban_bot = 'Я не могу заблокировать или разблокировать ботов.'
unban_top_roles = 'У Вас нет прав разблокировать этого пользователя.'
unban_user_is_not_blocked = 'Пользователь не заблокирован.'
unban_user_is_blocked = '{} разблокировал {}.'

# MUTE & UNMUTE

mute_bot = 'Я не могу замутить или размутить бота.'
mute_top_roles = 'У Вас нет прав замутить этого пользователя.'
mute_exceeding_days = 'Мут не должен привышать 7 дней.'
mute_user_is_muted = '{} выдал тайм-аут {} на {} по причине "{}".'

unmute_bot = 'Я не могу замутить или размутить бота.'
unmute_top_roles = 'У Вас нет прав размутить этого пользователя.'
unmute_user_is_not_muted = 'Пользователь не замучен.'
unmute_user_is_muted = 'Пользователь был успешно размучен.'


# RECRUITMENT

rec_no_right_to_decide = no + 'У Вас нет прав для этого взаимодействия.'
rec_channel_created = yes + 'Канал для заявки успешно создан. ({})'
rec_only_one_channel = no + 'У Вас уже есть одна заявка! ({})'

# STAFF

staff_vacation = yes + '{} ({}) был отправлен в отпуск.'
staff_warn_admin = yes + '{} ({}) получил предупреждение.'
staff_warn_user = yes + '{} ({}) получил предупреждение.'

# SUPPORT

support_only_two_channel = no + 'У Вас уже есть один тикет! ({})'
support_ticket_created = yes + 'Канал тикета успешно создан. ({})'

# ARCHIVE TICKETS

arch_deleted_archive_ticket = yes + 'Чистим архив состоящий из {} тикетов.'
arch_nothing_to_delete = no + 'Тикетов для очистки нет.'