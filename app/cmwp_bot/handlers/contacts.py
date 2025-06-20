from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import contacts_kb
from app.cmwp_bot.services.action_service import log_contacts_click

router = Router()


@router.callback_query(F.data == 'contacts')
async def show_contacts(callback: CallbackQuery):
    # TODO: возможность менять message из админки (подтягивать из бд текст и фото)
    
    await log_contacts_click(callback.from_user)

    await callback.message.edit_text(
        'Свяжитесь с нами напрямую:\n\n'
        'Email: tgbot-pds@cmwp.ru\n'
        'Телефон: +7 499 430-16-96\n\n'
        'Мы всегда готовы обсудить ваш проект и предложить оптимальное решение под ваши задачи.',
        reply_markup=contacts_kb,
        parse_mode='HTML'
    )
    await callback.answer()