from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import staff_wants_kb
from app.cmwp_bot.services.caption_service import get_text_block

router = Router()


@router.callback_query(F.data == 'staff_wants')
async def show_staff_wants(callback: CallbackQuery):
    content, _ = await get_text_block('staff_wants')

    await callback.message.edit_text(
        content,
        reply_markup=staff_wants_kb,
        parse_mode='HTML'
    )
    await callback.answer()