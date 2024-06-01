# SPDX-License-Identifier: MIT
# Copyright (c) 2018-2024 Amano LLC

from hydrogram import Client, filters
from hydrogram.types import ChatPrivileges, Message

from config import PREFIXES
from eduu.database.admins import check_if_antichannelpin, toggle_antichannelpin
from eduu.utils import commands
from eduu.utils.decorators import require_admin
from eduu.utils.localization import use_chat_lang


@Client.on_message(filters.command("antichannelpin", PREFIXES))
@require_admin(ChatPrivileges(can_pin_messages=True))
@use_chat_lang
async def setantichannelpin(c: Client, m: Message, strings):
    if len(m.text.split()) == 1:
        check_acp = await check_if_antichannelpin(m.chat.id)
        if not check_acp:
            await m.reply_text(strings("antichannelpin_status_disabled"))
        else:
            await m.reply_text(strings("antichannelpin_status_enabled"))
        return

    if m.command[1] == "on":
        await toggle_antichannelpin(m.chat.id, True)
        await m.reply_text(strings("antichannelpin_enabled"))
    elif m.command[1] == "off":
        await toggle_antichannelpin(m.chat.id, None)
        await m.reply_text(strings("antichannelpin_disabled"))
    else:
        await m.reply_text(strings("antichannelpin_invalid_arg"))


@Client.on_message(filters.linked_channel, group=-1)
async def acp_action(c: Client, m: Message):
    get_acp = await check_if_antichannelpin(m.chat.id)
    getmychatmember = await m.chat.get_member("me")
    if (get_acp and getmychatmember.can_pin_messages) is True:
        await m.unpin()


@Client.on_message(filters.command("pin", PREFIXES))
@require_admin(ChatPrivileges(can_pin_messages=True), allow_in_private=True)
async def pin(c: Client, m: Message):
    disable_notifications = "loud" not in m.text

    await c.pin_chat_message(
        m.chat.id,
        m.reply_to_message.id,
        disable_notification=disable_notifications,
        both_sides=True,
    )


@Client.on_message(filters.command("unpin", PREFIXES))
@require_admin(ChatPrivileges(can_pin_messages=True), allow_in_private=True)
async def unpin(c: Client, m: Message):
    await c.unpin_chat_message(m.chat.id, m.reply_to_message.id)


@Client.on_message(filters.command(["unpinall", "unpin all"], PREFIXES))
@require_admin(ChatPrivileges(can_pin_messages=True), allow_in_private=True)
async def unpinall(c: Client, m: Message):
    await c.unpin_all_chat_messages(m.chat.id)


commands.add_command("antichannelpin", "admin")
commands.add_command("pin", "admin")
commands.add_command("unpin", "admin")
commands.add_command("unpinall", "admin")
