from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.cmwp_bot.presentation.keyboards import office_price_kb
from app.cmwp_bot.services.action_service import log_office_price_download, log_user_action
from app.cmwp_bot.db.models import ActionType
from app.cmwp_bot.services.caption_service import get_text_block

router = Router()


@router.callback_query(F.data == 'office_price')
async def send_pdf_file(callback: CallbackQuery):
    await callback.message.delete()

    await log_office_price_download(callback.from_user)

    text, _ = await get_text_block('office_price')

    await callback.message.answer_document(
        document=FSInputFile('files/office_price.pdf'),
        caption=text,
        reply_markup=office_price_kb,
        parse_mode='HTML'
    )

    await callback.answer()