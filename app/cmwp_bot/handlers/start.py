from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from typing import AsyncGenerator

from app.cmwp_bot.presentation.registration import registration_dialog
from app.cmwp_bot.services.caption_service import get_text_block

router = Router()

active_dialogs: dict[int, AsyncGenerator] = {}


@router.message(CommandStart())
async def cmd_start(message: Message):
    text, _ = await get_text_block('welcome_message')

    await message.answer(text, parse_mode='HTML')

    dialog = registration_dialog(message)
    active_dialogs[message.from_user.id] = dialog
    await dialog.asend(None)


@router.message()
async def dialog_step(message: Message):
    dialog = active_dialogs.get(message.from_user.id)
    if dialog is None:
        return

    try:
        await dialog.asend(message)
    except StopAsyncIteration:
        del active_dialogs[message.from_user.id]