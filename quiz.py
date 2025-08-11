from random import choice

from db.user.get_user_record import get_user_record

from db.station.get_station_record import get_station_record
from db.station.add_station_record import add_station_record
from db.station.update_station_record import update_station_record

from db.words.words_by_lesson import get_words_by_lesson
from db.words.word_id import get_word_id

from mixed_keyboard import mixed_answer_keyboard

async def start_quiz_func(bot, user):
    user_data = await get_user_record(user)
    lessen = user_data['lesson']

    words = await get_words_by_lesson(lessen)
    words_keys = tuple(words.keys())
    words_values = tuple(words.values())
    
    word = choice(words_keys)
    word_translate = words[word]
    word_id = await get_word_id(word_translate, "words")

    user_station = await get_station_record(user)
    if user_station is None:
        await add_station_record(user, 'quiz', word_id)
    else:
        await update_station_record(user, 'quiz', word_id, 0, 0)
    
    keyboard = await mixed_answer_keyboard(word_translate, words_values)
    await bot.send_message(user, word, reply_markup=keyboard)
