import os
import random
import shutil
import requests
from dotenv import load_dotenv, find_dotenv
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import k_in


whitelist = [1047484838]

load_dotenv(find_dotenv())


class FSMGachi(StatesGroup):
    group_name = State()


def get_wall_posts(name):
    group_name = name
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=100&access_token={os.getenv('vk_api')}&v=5.131"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/107.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    src = response.json()
    posts = src["response"]["items"]

    if os.path.exists("gachi"):
        print("папки существуют")
    else:
        os.mkdir("gachi")

        for i in posts:
            post_id = i["id"]
            print(f"пост {post_id}")

            try:
                if "attachments" in i:
                    i = i["attachments"]

                    if i[0]["type"] == "photo":
                        if len(i) == 1:
                            url_img = i[0]["photo"]["sizes"][-1]["url"]
                            download(url_img)
                            print(f"{post_id} загружен через функцию 1")

                        else:
                            for i_ in i:
                                url_img_2 = i_["photo"]["sizes"][-1]["url"]
                                download(url_img_2)
                                print(f"{post_id} загружен через функцию 2")

                    else:
                        print(f"пост {post_id} не попал под нужные условия, скачен не был")

            except Exception:
                print(f"ошибка с постом {post_id}")

        return "все"


def download(url):
    name = url.split("/")[-1].split("?")[-2]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/107.0.0.0 Safari/537.36"}
    response = requests.get(url, headers, stream=True)
    with open("gachi/" + name, "wb") as r:
        for v in response.iter_content(1024 * 1024):
            r.write(v)


def delete1():
    dir_path = f"gachi/"
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Ошибка: %s : %s" % (dir_path, e.strerror))


async def gachi(message: types.Message):
    img_list = os.listdir("gachi")
    img_path = random.choice(img_list)
    await bot.send_photo(message.chat.id,
                         photo=open(f"gachi/{img_path}", "rb"),
                         reply_markup=k_in)


async def gachi2(callback: types.CallbackQuery):
    img_list = os.listdir("gachi")
    img_path = random.choice(img_list)
    await callback.bot.send_photo(callback.message.chat.id,
                                  photo=open(f"gachi/{img_path}", "rb"),
                                  reply_markup=k_in)


async def delete(message: types.Message):
    if message.from_user.id in whitelist:
        await bot.send_message(message.chat.id, "начинаю удалять")
        delete1()
        await bot.send_message(message.chat.id, "файлы удалены, чтобы загрузить новые: /загрузить")
    else:
        await bot.send_message(message.chat.id, "нет доступа", reply_markup=k_in)


async def upload(message: types.Message):
    if message.from_user.id in whitelist:
        await FSMGachi.group_name.set()
        await bot.send_message(message.chat.id, "группа")
    else:
        await bot.send_message(message.chat.id, "нет доступа", reply_markup=k_in)


async def group_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data3:
        data3["group_name"] = message.text
        await bot.send_message(message.chat.id, f"проверяю {data3['group_name']}")
        o = get_wall_posts(data3['group_name'])
        await bot.send_message(message.chat.id, f"{o}")
    await state.finish()


def register_handlers_gachi(dp: Dispatcher):
    dp.register_message_handler(gachi, commands=["гачи"])
    dp.register_message_handler(delete, commands=["удалить"])
    dp.register_message_handler(upload, commands=["загрузитьгачимем"], state=None)
    dp.register_message_handler(group_name, state=FSMGachi.group_name)
    dp.register_callback_query_handler(gachi2, text="gachi")
