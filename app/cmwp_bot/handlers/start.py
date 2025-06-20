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
        (
            "👋 Добро пожаловать в CMWP CONSTRUCTION!\n"
            "Здесь вы можете узнать:\n"
            "— Что сотрудники хотят видеть в офисе 2025 года\n"
            "— Какой он \"Офис вашей мечты?\" 👉 анкета за 20 секунд\n"
            "— Гайд по стоимости отделки офисов\n"
            "— Задать вопрос по вашей недвижимости\n"
            "— Наши контакты для связи\n\n"
            "Давайте начнём с короткого знакомства😉"
        )
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