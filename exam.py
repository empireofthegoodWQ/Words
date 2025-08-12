from random import choice


from db.user.get_user_record import get_user_record
from db.user.update_user_record import update_user_record

from db.station.get_station_record import get_station_record
from db.station.update_station_record import update_station_record

from db.station.add_station_record import add_station_record
from db.station.delete_station_record import delete_station_record

from db.words.words_test_by_lesson import get_words_test_by_lesson
from db.words.word_id import get_word_id


from mixed_keyboard import mixed_answer_keyboard
from keyboards import menu


async def start_exam_func(bot, user):
    user_data = await get_user_record(user)
    lesson = user_data['lesson']
    level = user_data['level']
    
    words1 = await get_words_test_by_lesson(lesson-2)
    words2 = await get_words_test_by_lesson(lesson-1)
    words3 = await get_words_test_by_lesson(lesson)

    words = {**words1,**words2,**words3}

    words_keys = tuple(words.keys())
    words_values = tuple(words.values())

    word = choice(words_keys)
    print(word)
    word_translate = words[word]
    print(word_translate)
    word_id = await get_word_id(word_translate, 'words_test')
    print(word_id)

    user_station = await get_station_record(user)

    if user_station is None:
        await add_station_record(user, 'exam', word_id)
    else:
        correct_answer = user_station['correct_answer']
        incorrect_answer = user_station['incorrect_answer']
        if incorrect_answer == 2:
            await bot.send_message(user, 'Иди учи слова!', reply_markup=menu)
            await delete_station_record(user)
            return
        if correct_answer == 1: #len(words_keys):# количество ответов совпадает с количеством вопросов
            level += 1
            await bot.send_message(
                user,
                'ПОЗДРАВЛЯЮ! Прошел экзамен',
                reply_markup=menu
            )
            await update_user_record(
                user,
                level=level,
                can_start_test=True,
                can_start_exam=False
            )
            await delete_station_record(user)
            return
        

        await update_station_record(user, station='exam', word_id=word_id,)
    
    keyboard = await mixed_answer_keyboard(word_translate, words_values)
    await bot.send_message(user, word, reply_markup=keyboard)
