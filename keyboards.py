
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stop_continue_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Завершить", callback_data="stop"),
        InlineKeyboardButton(text="Продолжить", callback_data="continuе"),
    ],
])


start_exam_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Пройти экзамен", callback_data="start_exam"),
    ],
])
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить Урок"),
            KeyboardButton(text="Начать Игру"),
            KeyboardButton(text="Пройти Тест"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)