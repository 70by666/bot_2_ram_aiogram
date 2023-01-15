import json
import string
import os
import random
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_other, k_in
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


whitelist = [1047484838, 1087968824]


class FSMRofl(StatesGroup):
    name = State()


async def starthelp2(message: types.Message):
    await bot.send_message(message.chat.id, "гачи мем или кот?", reply_markup=kb_other)


async def photo(message: types.Message):
    img_list = os.listdir("data/cats/")
    img_path = random.choice(img_list)
    await bot.send_photo(message.chat.id, photo=open(f"data/cats/{img_path}", "rb"),
                         reply_markup=k_in)


async def photo2(callback: types.CallbackQuery):
    img_list = os.listdir("data/cats/")
    img_path = random.choice(img_list)
    await callback.bot.send_photo(callback.message.chat.id,
                                  photo=open(f"data/cats/{img_path}", "rb"),
                                  reply_markup=k_in)
    await callback.answer()


async def get_id(message: types.Message):
    await bot.send_message(message.chat.id, message.from_user.id, reply_markup=k_in)


async def delkb(message: types.Message):
    mk = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, "удалил", reply_markup=mk)


async def nef(message: types.Message):
    await bot.send_message(message.chat.id, "сам ты нефор", reply_markup=k_in)


async def nocom(message: types.Message):
    await bot.send_message(message.chat.id, "нет такой команды", reply_markup=k_in)
    await message.delete()


async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(" ")}.intersection(
            set(json.load(open("mat.json", encoding="utf-8")))) != set():
        await message.reply("Такие вещи не говори!!!", reply_markup=k_in)
    elif message.text == "привет" or message.text == "Привет" or message.text == "Привет.":
        if message.from_user.id in whitelist:
            await FSMRofl.name.set()
            await bot.send_message(message.chat.id, "привет, как тебя зовут")
        else:
            await bot.send_message(message.chat.id, "у тебя нет доступа", reply_markup=k_in)


async def name_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data2:
        data2["name"] = message.text
        await bot.send_message(message.chat.id, f"пошел нахуй {data2['name']}!", reply_markup=k_in)
    await state.finish()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(get_id, commands=["ид"])
    dp.register_message_handler(photo, commands=["кот"])
    dp.register_message_handler(starthelp2, commands=["start", "help"])
    dp.register_message_handler(delkb, commands=["убратькнопки"])
    dp.register_message_handler(nef, lambda message: "нефор" in message.text)
    dp.register_message_handler(nocom, lambda message: message.text.startswith("/"))
    dp.register_message_handler(echo_send)
    dp.register_message_handler(name_text, state=FSMRofl.name)
    dp.register_callback_query_handler(photo2, text="kot")
