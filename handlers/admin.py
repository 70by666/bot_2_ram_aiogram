from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from data import sqlite_d
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inlinemem import k_in


whitelist = [1047484838]


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()


async def cm_start(message: types.Message):
    if message.from_user.id in whitelist:
        await FSMAdmin.photo.set()
        await message.reply("загрузи фото")
    else:
        await bot.send_message(message.chat.id, "у тебя нет доступа", reply_markup=k_in)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0]["file_id"]
        await FSMAdmin.next()
        await message.reply("теперь название")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await sqlite_d.sql_add_command(state)
    await state.finish()
    await message.reply("готово")


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None
    await state.finish()
    await message.reply("ладно, ок", reply_markup=k_in)


async def test_zag_pol(message: types.Message):
    if message.from_user.id in whitelist:
        await sqlite_d.test_zag_pol(message)
    else:
        await bot.send_message(message.chat.id, "у тебя нет доступа", reply_markup=k_in)


async def del_call(callback_query: types.CallbackQuery):
    await sqlite_d.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text="удалено", show_alert=True)


async def delete_i(message: types.Message):
    if message.from_user.id in whitelist:
        read = await sqlite_d.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f"что я написал: {ret[1]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"удалить {ret[1]}", callback_data=f"del {ret[1]}")))
    else:
        await bot.send_message(message.chat.id, "у тебя нет доступа", reply_markup=k_in)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands="загрузить", state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="стоп")
    dp.register_message_handler(cancel_handler, Text(equals="стоп", ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(test_zag_pol, commands="покажи")
    dp.register_message_handler(delete_i, commands="удалить")
    dp.register_callback_query_handler(del_call, Text(startswith="del "))
