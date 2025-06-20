from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import office_price_kb

router = Router()


@router.callback_query(F.data == 'office_price')
async def show_contacts(callback: CallbackQuery):
    # TODO: возможность менять message из админки (подтягивать из бд текст)
    
    await callback.message.edit_text(
        "Вот ваш файл:",
        reply_markup=office_price_kb,
        parse_mode='HTML'
    )
    await callback.answer()