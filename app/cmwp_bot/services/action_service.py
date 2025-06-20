import datetime as dt
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, User as TelegramUser

from app.cmwp_bot.db.models import SurveyAnswer, UserAction, ActionType
from app.cmwp_bot.db.repo import get_session
from app.cmwp_bot.services.email_service import send_discuss_email
from app.cmwp_bot.services.survey_service import delete_answers_for_user, get_answers_for_user
from app.cmwp_bot.services.user_service import create_or_update_user, get_admin_ids


async def create_user_action(
    session: AsyncSession,
    user_id: int,
    action_type: ActionType,
    payload: dict | None = None
) -> UserAction:
    action = UserAction(
        user_id=user_id,
        type=action_type,
        payload=payload or {},
        created_at=dt.datetime.utcnow()
    )
    session.add(action)
    return action


async def log_user_action(
    tg_user,
    action_type: ActionType,
    payload: dict | None = None
) -> None:
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=tg_user.id,
            first_name=tg_user.first_name or '',
            last_name=tg_user.last_name or '',
        )
        await session.flush()
        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=action_type,
            payload=payload
        )


async def log_survey_started(tg_user):
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=tg_user.id,
            first_name=tg_user.first_name or '',
            last_name=tg_user.last_name or '',
        )
        await delete_answers_for_user(session, user.id)
        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.SURVEY_STARTED
        )


async def log_survey_answer(tg_user, question_no: int, answer_text: str):
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=tg_user.id,
            first_name=tg_user.first_name or '',
            last_name=tg_user.last_name or '',
        )
        session.add(SurveyAnswer(
            user_id=user.id,
            question_no=question_no,
            answer=answer_text
        ))


async def log_survey_completed(tg_user):
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=tg_user.id,
            first_name=tg_user.first_name or '',
            last_name=tg_user.last_name or '',
        )
        user.survey_completed_at = dt.datetime.utcnow()
        session.add(user)
        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.SURVEY_COMPLETED
        )


async def log_get_plan(tg_user) -> tuple:
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=tg_user.id,
            first_name=tg_user.first_name or '',
            last_name=tg_user.last_name or '',
        )
        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.CLICK_GET_PLAN
        )
        answers = await get_answers_for_user(session, user.id)
        admin_ids = await get_admin_ids(session)
        return user, answers, admin_ids


async def log_contacts_click(from_user: TelegramUser):
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=from_user.id,
            first_name=from_user.first_name or '',
            last_name=from_user.last_name or '',
        )
        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.CLICK_CONTACTS,
        )


async def log_discuss_project(tg_user: TelegramUser) -> tuple:
    async with get_session() as session:
        user = await create_or_update_user(
            session=session,
            tg_id=tg_user.id,
            first_name=tg_user.first_name or '',
            last_name=tg_user.last_name or '',
        )
        await session.flush()

        await create_user_action(
            session=session,
            user_id=user.id,
            action_type=ActionType.CLICK_DISCUSS
        )

        admin_ids = await get_admin_ids(session)
        return user, admin_ids
