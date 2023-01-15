from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client


async def starthelp(message: types.Message):
    await bot.send_message(message.chat.id, "ответ на старт или хелп",
                           reply_markup=kb_client)


async def primer(message: types.Message):
    await bot.send_message(message.chat.id, "ответ на команду primer")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(starthelp, commands=["start", "help"])
    dp.register_message_handler(primer, commands=["primer"])
