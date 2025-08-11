from random import choice, sample
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def mixed_answer_keyboard(correct_ans, words_values):
    buttons = [
        KeyboardButton(text=correct_ans),
        KeyboardButton(text=choice(words_values)),
        KeyboardButton(text=choice(words_values))
    ]
    buttons = sample(buttons, len(buttons))

    return ReplyKeyboardMarkup(
        keyboard=[
            buttons,
            [KeyboardButton(text='STOP')]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
