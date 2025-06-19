from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence

from app.cmwp_bot.db.models import SurveyAnswer


async def get_answers_for_user(session: AsyncSession, user_id: int) -> Sequence[SurveyAnswer]:
    result = await session.scalars(
        select(SurveyAnswer)
        .where(SurveyAnswer.user_id == user_id)
        .order_by(SurveyAnswer.question_no)
    )
    return result.all()


async def delete_answers_for_user(session: AsyncSession, user_id: int) -> None:
    await session.execute(
        delete(SurveyAnswer).where(SurveyAnswer.user_id == user_id)
    )