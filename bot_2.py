from aiogram.utils import executor
from create_bot import dp
from handlers import admin, other, gachi
from data import sqlite_d


async def on_startup(_):
    print("бот работает")
    sqlite_d.sql_start()


admin.register_handlers_admin(dp)
gachi.register_handlers_gachi(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
