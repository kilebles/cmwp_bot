from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.cmwp_bot.settings import config
from app.cmwp_bot.handlers import start
from app.cmwp_bot.handlers import contacts
from app.cmwp_bot.handlers import back
from app.cmwp_bot.handlers import staff_wants
from app.cmwp_bot.handlers import how_helpful
from app.cmwp_bot.handlers import ideal

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(contacts.router)
dp.include_router(back.router)
dp.include_router(staff_wants.router)
dp.include_router(how_helpful.router)
dp.include_router(ideal.router)