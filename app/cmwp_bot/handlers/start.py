from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from typing import AsyncGenerator

from app.cmwp_bot.presentation.registration import registration_dialog

router = Router()

active_dialogs: dict[int, AsyncGenerator] = {}


@router.message(CommandStart())
async def cmd_start(message: Message):
    # TODO: возможность менять message из админки (подтягивать из бд текст)
    
    await message.answer(
        "Добро пожаловать!\n"
        "Здесь вы можете:\n"
        "— Узнать, что сотрудники хотят видеть в офисах 2025 года\n"
        "— Пройти анкету и получить подборку «Идеальный офис под ваши задачи»\n"
        "— Получить обзор по стоимости отделки офисов\n"
        "— Задать вопрос по вашей недвижимости\n"
        "— Контакты для связи\n\n"
        "🔹 Начнём с короткого знакомства"
    )
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