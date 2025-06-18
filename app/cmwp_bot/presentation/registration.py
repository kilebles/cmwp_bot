import re
import asyncio
from contextlib import suppress

from aiogram.types import Message, ReplyKeyboardRemove

from app.cmwp_bot.presentation.keyboards import main_menu_kb, phone_request_kb
from app.cmwp_bot.services.user_service import create_or_update_user
from app.cmwp_bot.services.action_service import create_user_action
from app.cmwp_bot.db.repo import get_session
from app.cmwp_bot.db.models import ActionType


def is_russian(text: str) -> bool:
    return bool(re.fullmatch(r'[А-Яа-яЁё\- ]{2,50}', text.strip()))


def normalize_phone(text: str) -> str:
    return re.sub(r'[^\d+]', '', text)


def is_valid_phone(text: str) -> bool:
    phone = normalize_phone(text)
    return bool(re.fullmatch(r'^\+7\d{10}$', phone))


async def send_temp_warning(message: Message, text: str, delay: float = 3.0):
    """Автоудаление предупреждения"""
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
    await company_msg.answer('Введите ваш телефон:', reply_markup=phone_request_kb)
    while True:
        phone_msg: Message = yield

        if phone_msg.contact and phone_msg.contact.phone_number:
            phone = normalize_phone(phone_msg.contact.phone_number)
        else:
            phone = normalize_phone(phone_msg.text or '')

        if is_valid_phone(phone):
            user_data['phone'] = phone
            break

        await send_temp_warning(phone_msg, '❌ Телефон должен быть в формате +79123456789. Попробуйте снова.')

    # Сохраняем пользователя в БД
    from_user = phone_msg.from_user

    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=from_user.id,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            company=user_data['company'],
            phone=user_data['phone'],
        )
        
        await session.flush()

        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.REGISTRATION_FINISHED,
        )

    # Завершение
    await phone_msg.answer(f'Спасибо, {user_data["first_name"]}!', reply_markup=ReplyKeyboardRemove())

    await phone_msg.answer(
        f"Теперь вы можете выбрать, что вам интересно:\n\n",
        reply_markup=main_menu_kb
    )
