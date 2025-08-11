from db_py.db_utils import *
from random import choice
from keyboards import menu
from mixed_keyboard import mixed_answer_keyboard

async def start_exam_func(bot, user):
    user_data = get_user_data(user)
    lesson = user_data['lesson']
    level = user_data['level']

    if user_data['can_start_exam'] == False:
        return
    
    words1 = get_words_test_by_lesson(lesson-2)
    words2 = get_words_test_by_lesson(lesson-1)
    words3 = get_words_test_by_lesson(lesson)

    words = {**words1,**words2,**words3}

    words_keys = tuple(words.keys())
    words_values = tuple(words.values())

    word = choice(words_keys)
    word_translate = words[word]
    word_id = await get_word_id(word_translate, 'exam')

    user_station = await get_station_data(user)

    if user_station is None:
        await add_station_data(user, 'exam', word_id)
    else:
        correct_answer = user_station['correct_answer']
        incorrect_answer = user_station['incorrect_answer']
        if incorrect_answer == 2:
            await bot.send_message(user, 'Иди учи слова!')
            await delete_station_data(user)
            return
        if correct_answer == 1: #len(words_keys):# количество ответов совпадает с количеством вопросов
            level += 1
            await bot.send_message(
                user,
                'ПОЗДРАВЛЯЮ! Прошел экзамен',
                reply_markup=menu
            )
            await update_user_data(user, level=level)
            return
        await update_station_data(user, 'test', word_id, correct_answer, incorrect_answer)

    keyboard = await mixed_answer_keyboard(word_translate, words_values)
    await bot.send_message(user, word, reply_markup=keyboard)
