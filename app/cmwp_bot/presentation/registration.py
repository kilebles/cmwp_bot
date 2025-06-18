import re
import asyncio

from contextlib import suppress
from aiogram.types import Message

from app.cmwp_bot.presentation.keyboards import main_menu_kb


def is_russian(text: str) -> bool:
    return bool(re.fullmatch(r'[А-Яа-яЁё\- ]{2,50}', text.strip()))


def normalize_phone(text: str) -> str:
    return re.sub(r'[^\d+]', '', text)


def is_valid_phone(text: str) -> bool:
    phone = normalize_phone(text)
    return bool(re.fullmatch(r'^\+7\d{10}$', phone))


async def send_temp_warning(message: Message, text: str, delay: float = 3.0):
    """Автоудаления предупреждения"""
    warn = await message.answer(text)

    async def auto_delete():
        await asyncio.sleep(delay)
        with suppress(Exception):
            await warn.delete()

    asyncio.create_task(auto_delete())


async def registration_dialog(start_message: Message):
    """Регистрация пользователя с валидацией"""

    user_data = {}

    # Имя
    await start_message.answer('Введите ваше имя:')
    while True:
        name_msg: Message = yield
        if is_russian(name_msg.text):
            user_data['first_name'] = name_msg.text.strip()
            break
        await send_temp_warning(name_msg, '❌ Имя должно содержать только русские буквы. Попробуйте снова.')

    # Фамилия
    await name_msg.answer('Введите вашу фамилию:')
    while True:
        last_msg: Message = yield
        if is_russian(last_msg.text):
            user_data['last_name'] = last_msg.text.strip()
            break
        await send_temp_warning(last_msg, '❌ Фамилия должна содержать только русские буквы.')

    # Компания
    await last_msg.answer('Введите название вашей компании:')
    company_msg: Message = yield
    user_data['company'] = company_msg.text.strip()

    # Телефон
    await company_msg.answer('Введите ваш телефон:')
    while True:
        phone_msg: Message = yield
        if is_valid_phone(phone_msg.text):
            user_data['phone'] = phone_msg.text.strip()
            break
        await send_temp_warning(phone_msg, '❌ Телефон должен быть в формате +79123456789. Попробуйте снова.')

    # Завершение
    await phone_msg.answer(
        f"Спасибо, {user_data['first_name']}!\n"
        f"Теперь вы можете выбрать, что вам интересно:",
        reply_markup=main_menu_kb
    )
