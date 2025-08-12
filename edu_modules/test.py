from random import choice

from db.user.get_user_record import get_user_record
from db.user.update_user_record import update_user_record

from db.station.get_station_record import get_station_record
from db.station.update_station_record import update_station_record

from db.station.add_station_record import add_station_record
from db.station.delete_station_record import delete_station_record

from db.words.words_test_by_lesson import get_words_test_by_lesson
from db.words.word_id import get_word_id


from keyboards import menu, start_exam_keyboard
from mixed_keyboard import mixed_answer_keyboard


async def start_test_func(bot, user):
    user_data = await get_user_record(user)
    lesson = user_data['lesson']

    words = await get_words_test_by_lesson(lesson)
    words_keys = tuple(words.keys())
    words_values = tuple(words.values())
    
    word = choice(words_keys)
    word_translate = words[word]
    word_id = await get_word_id(word, 'words_test')

    user_station = await get_station_record(user)

    if user_station is None:
        await add_station_record(user, 'test', word_id)
    else:
        correct_answer = user_station['correct_answer']
        incorrect_answer = user_station['incorrect_answer']
        if incorrect_answer == 3:
            await bot.send_message(user, 'Иди учи слова!')
            await delete_station_record(user)
            return
        if correct_answer == 1: #len(words_keys):# количество ответов совпадает с количеством вопросов
            lesson += 1
            await bot.send_message(
                user,
                'ПОЗДРАВЛЯЮ! Прошел тест',
                reply_markup=menu
            )
            await update_user_record(user, lesson=lesson)
            if lesson > 0 and lesson % 3 == 0:
                await bot.send_message(
                    user,
                    "Чтобы пройти дальше нужно пройти экзамен",
                    reply_markup=start_exam_keyboard
                )
            await delete_station_record(user)
            return
        await update_station_record(user, word_id=word_id, correct_answer=correct_answer, incorrect_answer=incorrect_answer)

    keyboard = await mixed_answer_keyboard(word_translate, words_values)
    await bot.send_message(user, word, reply_markup=keyboard)

