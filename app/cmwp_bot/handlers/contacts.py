from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import contacts_kb
from app.cmwp_bot.db.repo import get_session
from app.cmwp_bot.services.user_service import create_or_update_user
from app.cmwp_bot.services.action_service import create_user_action
from app.cmwp_bot.db.models import ActionType

router = Router()


@router.callback_query(F.data == 'contacts')
async def show_contacts(callback: CallbackQuery):
    # TODO: возможность менять message из админки (подтягивать из бд текст)
    
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
            action_type=ActionType.CLICK_CONTACTS
        )

    await callback.message.edit_text(
        'Свяжитесь с нами напрямую:\n\n'
        'Email: tgbot-pds@cmwp.ru\n'
        'Телефон: +7 499 430-16-96\n\n'
        'Мы всегда готовы обсудить ваш проект и предложить оптимальное решение под ваши задачи.',
        reply_markup=contacts_kb,
        parse_mode='HTML'
    )
    await callback.answer()
