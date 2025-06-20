from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from typing import AsyncGenerator

from app.cmwp_bot.presentation.keyboards import make_keyboard, get_plan_kb
from app.cmwp_bot.services.caption_service import get_text_block
from app.cmwp_bot.services.email_service import send_plan_email
from app.cmwp_bot.services.action_service import log_get_plan, log_survey_answer, log_survey_completed, log_survey_started

router = Router()
active_surveys: dict[int, AsyncGenerator] = {}


@router.callback_query(F.data == 'ideal')
async def start_survey(callback: CallbackQuery):
    await log_survey_started(callback.from_user)

    await callback.message.delete()
    msg = await callback.message.answer("...")
    gen = ideal_office_survey(msg, callback.from_user)
    active_surveys[callback.from_user.id] = gen
    await gen.asend(None)
    await callback.answer()


@router.callback_query(F.data.startswith('q'))
async def survey_step(callback: CallbackQuery):
    gen = active_surveys.get(callback.from_user.id)
    if not gen:
        await callback.answer('Ошибка. Начните заново.', show_alert=True)
        return
    try:
        await gen.asend(callback)
    except StopAsyncIteration:
        del active_surveys[callback.from_user.id]
    await callback.answer()


async def ideal_office_survey(msg: Message, from_user) -> AsyncGenerator:
    questions = [
        ("Какая площадь вашего объекта?", ["До 1000 м²", "1000–5000 м²", "Более 5000 м²"]),
        ("Сколько этажей в вашем офисе?", ["1 этаж", "2–5 этажей", "Более 5 этажей"]),
        ("Где расположен объект?", ["Москва", "Московская область", "Другой регион"]),
        ("Какое текущее состояние офиса?", ["Черновая отделка", "Требуется перепланировка", "Нужна идея", "Другое"]),
        ("Сколько сотрудников работает в компании?", ["Менее 100", "100–500", "Более 500"]),
        ("Какой формат офиса вам больше подходит?", ["Open-space", "Кабинетная система", "Гибридный", "Другое"]),
        ("Какой стиль офиса ближе вашей команде?", [
            "Современный минимализм", "Уютный и домашний",
            "Хай-тек/Техно", "Бизнес",
            "Не знаю, хочу вдохновение"
        ])
    ]

    for i, (q_text, options) in enumerate(questions, start=1):
        kb = make_keyboard(options, f'q{i}')
        msg = await msg.edit_text(f"<b>{i}.</b> {q_text}", reply_markup=kb, parse_mode='HTML')
        callback: CallbackQuery = yield

        answer_text = callback.data.split(':', 1)[-1]
        await log_survey_answer(from_user, i, answer_text)

    await log_survey_completed(from_user)

    text, photo = await get_text_block('survey_result')
    
    await callback.message.delete()
    await msg.answer_photo(
        photo=photo or 'https://i.postimg.cc/8zr0f4Zy/1737985155837-2.jpg',
        caption=text,
        reply_markup=get_plan_kb,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'get_plan')
async def plan_answer(callback: CallbackQuery):
    """Коммит в бд, рассылка админам в тг и на почту"""
    
    from_user = callback.from_user
    bot = callback.message.bot

    user, answers, admin_ids = await log_get_plan(from_user)

    questions_map = {
        1: "Какая площадь вашего объекта?",
        2: "Сколько этажей в вашем офисе?",
        3: "Где расположен объект?",
        4: "Какое текущее состояние офиса?",
        5: "Сколько сотрудников работает в компании?",
        6: "Какой формат офиса вам больше подходит?",
        7: "Какой стиль офиса ближе вашей команде?",
    }

    answers_text = "\n".join(
        f"<b>{i}. {questions_map.get(ans.question_no, 'Вопрос')}</b>\n— {ans.answer}"
        for i, ans in enumerate(answers, start=1)
    )

    full_name = f'{user.first_name or ""} {user.last_name or ""}'.strip()
    username_link = f'https://t.me/{from_user.username}' if from_user.username else '—'

    text = (
        f'👤 <b>{full_name}</b>\n'
        f'хочет получить план организации пространства офиса\n\n'
        f'Компания: {user.company or "—"}\n'
        f'Телефон: {user.phone or "—"}\n'
        f'Профиль: {username_link}\n\n'
        f'📋 <b>Ответы на анкету:</b>\n{answers_text}'
    )

    for admin_id in admin_ids:
        await bot.send_message(admin_id, text, parse_mode='HTML')

    await send_plan_email(
        full_name=full_name,
        username_link=username_link,
        phone=user.phone or "—",
        company=user.company or "—",
        answers_text=answers_text.replace('<b>', '').replace('</b>', '')
    )

    await callback.message.answer(
        'Заявка принята. Мы уже готовим для вас план. Скоро свяжемся!',
        parse_mode='HTML'
    )
    await callback.answer()