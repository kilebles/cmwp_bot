from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.cmwp_bot.db.models import User
import datetime as dt


async def create_or_update_user(
    session: AsyncSession,
    tg_id: int,
    first_name: str,
    last_name: str,
    company: str,
    phone: str
) -> User:
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one_or_none()

    now = dt.datetime.utcnow()

    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.company = company
        user.phone = phone
        user.last_activity_at = now
    else:
        user = User(
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
            company=company,
            phone=phone,
            registered_at=now,
            last_activity_at=now
        )
        session.add(user)

    return user