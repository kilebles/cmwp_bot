from sqlalchemy.ext.asyncio import AsyncSession
from app.cmwp_bot.db.models import UserAction, ActionType
import datetime as dt


async def create_user_action(
    session: AsyncSession,
    user_id: int,
    action_type: ActionType,
    payload: dict | None = None
):
    action = UserAction(
        user_id=user_id,
        type=action_type,
        payload=payload or {},
        created_at=dt.datetime.utcnow()
    )
    session.add(action)
    return action