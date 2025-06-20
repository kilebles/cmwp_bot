from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.cmwp_bot.presentation.keyboards import office_price_kb
from app.cmwp_bot.services.action_service import log_user_action
from app.cmwp_bot.db.models import ActionType

router = Router()


@router.callback_query(F.data == 'office_price')
async def send_pdf_file(callback: CallbackQuery):
    await callback.message.delete()

    await log_user_action(
        tg_user=callback.from_user,
        action_type=ActionType.CLICK_PRICES
    )

    await callback.message.answer_document(
        document=FSInputFile('files/office_price.pdf'),
        caption='📄 Ознакомьтесь с прайс-листом на офисы:',
        reply_markup=office_price_kb,
        parse_mode='HTML'
    )

    await callback.answer()
