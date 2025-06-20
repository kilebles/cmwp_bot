from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import how_helpful_kb
from app.cmwp_bot.services.email_service import send_discuss_email
from app.cmwp_bot.services.action_service import log_discuss_project

router = Router()


@router.callback_query(F.data == 'how_helpful')
async def show_contacts(callback: CallbackQuery):
    # TODO: возможность менять message из админки (подтягивать из бд текст и фото)
    
    await callback.message.delete()
    await callback.message.answer_photo(
        photo='https://i.postimg.cc/Nfss4q1y/FR7A1162.jpg',
        caption=(
            "<b>Человек — мера всех проектов.</b>\n\n"
            "Поэтому мы создаём коммерческие пространства для бизнеса и для людей — с первых идей до ввода в эксплуатацию.\n\n"
            "<b>Наши компетенции:</b>\n"
            "— Технический аудит помещений\n"
            "— Разработка концепции\n"
            "— Стратегия организации рабочих пространств\n"
            "— Управление строительством и отделкой\n"
            "— Контроль бюджета, сроков и качества\n\n"
            "<b>Нам доверяют:</b> Альфа-Банк, Лукойл, Huawei, Nestlé, НЛМК, РЖД, Газпром, ВТБ и другие лидеры рынка.\n\n"
            "Каждый проект — с индивидуальной стратегией под задачи бизнеса."
        ),
        reply_markup=how_helpful_kb,
        parse_mode='HTML'
    )
    await callback.answer()
    

@router.callback_query(F.data == 'discuss_project')
async def contacts_answer(callback: CallbackQuery):
    """Коммит в бд, рассылка админам в тг и на почту"""
    
    from_user = callback.from_user
    bot = callback.bot

    user, admin_ids = await log_discuss_project(from_user)

    full_name = f'{user.first_name or ""} {user.last_name or ""}'.strip()
    username_link = f'https://t.me/{from_user.username}' if from_user.username else '—'

    text = (
        f'👤 <b>{full_name}</b>\n'
        f'хочет обсудить проект\n\n'
        f'Компания: {user.company or "—"}\n'
        f'Телефон: {user.phone or "—"}\n'
        f'Профиль: {username_link}'
    )

    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, text, parse_mode='HTML')
        except Exception:
            pass

    await send_discuss_email(
        full_name=full_name,
        username_link=username_link,
        phone=user.phone or "—",
        company=user.company or "—"
    )

    await callback.message.answer(
        'Ваша заявка отправлена, мы скоро свяжемся с вами!'
    )
    await callback.answer()