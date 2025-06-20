from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import contacts_kb
from app.cmwp_bot.services.action_service import log_contacts_click
from app.cmwp_bot.services.caption_service import get_text_block

router = Router()


@router.callback_query(F.data == 'contacts')
async def show_contacts(callback: CallbackQuery):
    await log_contacts_click(callback.from_user)

    text, _ = await get_text_block('contacts')

    await callback.message.edit_text(
        text,
        reply_markup=contacts_kb,
        parse_mode='HTML'
    )
    await callback.answer()