from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


k_in = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Кот", callback_data="kot"),
                                             InlineKeyboardButton(text="Гачи", callback_data="gachi"))
