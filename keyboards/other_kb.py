from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton("/кот")
b2 = KeyboardButton("/гачи")
b3 = KeyboardButton("/убратькнопки")


kb_other = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_other.add(b1, b2, b3)
