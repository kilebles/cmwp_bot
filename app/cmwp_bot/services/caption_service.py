from app.cmwp_bot.db.repo import get_session
from app.cmwp_bot.db.models import StaticText
from sqlalchemy import select


async def get_text_block(key: str) -> tuple[str, str | None]:
    async with get_session() as session:
        result = await session.execute(select(StaticText).where(StaticText.key == key))
        obj = result.scalar_one_or_none()
        if obj:
            return obj.content, obj.photo_url
        return f'❌ Нет текста <b>{key}</b> не найден', None