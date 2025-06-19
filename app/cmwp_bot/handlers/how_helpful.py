from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_bot.presentation.keyboards import how_helpful_kb
from app.cmwp_bot.db.repo import get_session
from app.cmwp_bot.services.user_service import create_or_update_user
from app.cmwp_bot.services.action_service import create_user_action
from app.cmwp_bot.db.models import ActionType
from app.cmwp_bot.services.user_service import get_admin_ids

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
    from_user = callback.from_user
    bot = callback.bot

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
            action_type=ActionType.CLICK_DISCUSS
        )

        admin_ids = await get_admin_ids(session)
        full_name = f'{user.first_name or ""} {user.last_name or ""}'.strip()
        text = (
            f'👤 <b>{full_name}</b>\n'
            f'хочет обсудить проект\n\n'
            f'Компания: {user.company or "—"}\n'
            f'Телефон: {user.phone or "—"}'
        )
        for admin_id in admin_ids:
            try:
                await bot.send_message(admin_id, text)
            except Exception:
                pass

    await callback.message.answer(
        'Ваша заявка отправлена, мы скоро свяжемся с вами!'
    )
    await callback.answer()