import datetime as dt
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from typing import AsyncGenerator

from app.cmwp_bot.presentation.keyboards import make_keyboard, get_plan_kb
from app.cmwp_bot.db.repo import get_session
from app.cmwp_bot.services.user_service import create_or_update_user
from app.cmwp_bot.services.action_service import create_user_action
from app.cmwp_bot.db.models import ActionType

router = Router()
active_surveys: dict[int, AsyncGenerator] = {}


@router.callback_query(F.data == 'ideal')
async def start_survey(callback: CallbackQuery):
    from_user = callback.from_user

    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=from_user.id,
            first_name=from_user.first_name or '',
            last_name=from_user.last_name or '',
            company='',
            phone='',
        )
        await session.flush()
        await create_user_action(session, user_id=user.id, action_type=ActionType.SURVEY_STARTED)

    await callback.message.delete()
    msg = await callback.message.answer("...")
    gen = ideal_office_survey(msg, from_user)
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
            "Современный минимализм", "Тёплый и домашний",
            "Хай-тек/техногенный", "Классический бизнес-стиль",
            "Не знаю, хочу вдохновение"
        ])
    ]

    for i, (q_text, options) in enumerate(questions, start=1):
        kb = make_keyboard(options, f'q{i}')
        msg = await msg.edit_text(f"<b>{i}.</b> {q_text}", reply_markup=kb, parse_mode='HTML')
        callback: CallbackQuery = yield

    await msg.delete()

    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=from_user.id,
            first_name=from_user.first_name or '',
            last_name=from_user.last_name or '',
        )

        user.survey_completed_at = dt.datetime.utcnow()
        session.add(user)
        await session.flush()

        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.SURVEY_COMPLETED
        )

    await msg.answer_photo(
        photo='https://i.postimg.cc/8zr0f4Zy/1737985155837-2.jpg',
        caption=(
            "Ваш идеальный офис — это не квадратные метры. Это ваша идея, ожившая в пространстве.\n"
            "Вы не просто прошли анкету.\n"
            "Вы на пороге создания пространства, которое отражает мышление вашей команды, ценности вашей компании, будущее вашей культуры.\n"
            "Только представьте:\n"
            "— Офис, в котором дышится легко — не только из-за воздуха, но из-за атмосферы.\n"
            "— Дизайн, в котором каждая линия продумана — стильный и аутентичный.\n"
            "— Пространство, в котором не нужно «адаптироваться» — оно работает на людей, потому что создано изнутри, с пониманием.\n"
            "— Люди хотят туда возвращаться. Кандидаты хотят работать только у вас. Команда раскрывает потенциал, потому что пространство помогает, а не мешает.\n"
            "Это не просто комфорт.\n"
            "Это стратегический актив. Это репутация. Это ваше конкурентное преимущество, незаметное, но сильное.\n"
            "А теперь вопрос, который меняет игру:\n"
            "Хотите получить не просто план, а визуализированное пространство, в которое захочется влюбиться — вам, вашей команде и вашему CEO?"
        ),
        reply_markup=get_plan_kb,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'get_plan')
async def plan_answer(callback: CallbackQuery):
    await callback.message.answer(
        'Заявка принята. Мы уже готовим для вас план. Скоро свяжемся!',
        parse_mode='HTML'
    )

    from_user = callback.from_user
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=from_user.id,
            first_name=from_user.first_name or '',
            last_name=from_user.last_name or '',
        )
        await session.flush()
        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.CLICK_GET_PLAN
        )

    await callback.answer()
