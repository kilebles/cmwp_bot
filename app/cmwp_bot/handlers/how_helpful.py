from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import how_helpful_kb

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
    await callback.message.answer(
        'Ваша заявка отправлена, мы скоро свяжемся с вами!',
        parse_mode='HTML'
    )
    await callback.answer()
