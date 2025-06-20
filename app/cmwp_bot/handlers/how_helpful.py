from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import how_helpful_kb
from app.cmwp_bot.services.caption_service import get_text_block
from app.cmwp_bot.services.email_service import send_discuss_email
from app.cmwp_bot.services.action_service import log_discuss_project

router = Router()


@router.callback_query(F.data == 'how_helpful')
async def show_contacts(callback: CallbackQuery):
    await callback.message.delete()

    text, photo = await get_text_block('how_helpful')

    await callback.message.answer_photo(
        photo=photo or 'https://i.postimg.cc/Nfss4q1y/FR7A1162.jpg',
        caption=text,
        reply_markup=how_helpful_kb,
        parse_mode='HTML'
    )
    await callback.answer()
    

@router.callback_query(F.data == 'discuss_project')
async def contacts_answer(callback: CallbackQuery):
    """Коммит в бд, рассылка админам в тг и на почту"""
    
    from_user = callback.from_user
    bot = callback.bot

    user, admin_ids, answers_text = await log_discuss_project(from_user)

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
        company=user.company or "—",
        answers_text=answers_text
    )

    await callback.message.answer(
        'Ваша заявка отправлена, мы скоро свяжемся с вами!'
    )
    await callback.answer()