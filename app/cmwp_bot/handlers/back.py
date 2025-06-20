from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import main_menu_kb

router = Router()


@router.callback_query(F.data == 'back')
async def show_contacts(callback: CallbackQuery):
    await callback.message.delete() 
    await callback.message.answer(
        'Выберите опцию:',
        reply_markup=main_menu_kb
    )
    await callback.answer()