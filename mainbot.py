from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from asyncio import run


from db.user.add_user import add_user
from db.user.get_user_record import get_user_record

from db.station.add_station_record import add_station_record
from db.station.update_station_record import update_station_record
from db.station.get_station_record import get_station_record
from db.station.delete_station_record import delete_station_record

from db.words.word_by_id import get_word_by_id


from exam import start_exam_func
from test import start_test_func
from quiz import start_quiz_func
from lesson import get_lesson_func
from keyboards import menu, stop_continue_keyboard, start_exam_keyboard


from API import __APIBOT__

bot = Bot(token=__APIBOT__, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    user = message.from_user.id
    await message.reply('Привет! Я бот на aiogram!', reply_markup=menu)
    
    user_data = await get_user_record(user)
    if user_data is None:
        await add_user(user)

@dp.message(F.text == 'Получить Урок')
async def gs(message: types.Message):
    user = message.from_user.id
    user_station = await get_station_record(user)

    if user_station is not None:
        station = user_station['station']

        if station in ('test', 'exam'):
            await message.reply('Во время теста/экзамена нельзя этим пользоаться!')
            return
        await get_lesson_func(bot, user)
    
        
    await get_lesson_func(bot, user) 

@dp.message(F.text == 'Начать Игру')
async def sq(message: types.Message):
    user = message.from_user.id
    user_station = await get_station_record(user)

    if user_station is not None:
        station = user_station['station']

        if station == 'quiz':
            await message.reply('Вы уже играете в игру!')
        elif station in ('test', 'exam'):
            await message.reply('Завершите игру что бы начать этот режим!')
        return
        
    await start_quiz_func(bot, user)

@dp.message(F.text == 'Пройти Тест')
async def sq(message: types.Message):
    user = message.from_user.id
    user_station = await get_station_record(user)
    user_data = await get_user_record(user)

    if user_data['can_start_test'] == False:
        await message.reply('Вам нужно пройти экзамен чтобы двигаться дальше', reply_markup=start_exam_keyboard)
        return

    if user_station is not None:
        station = user_station['station']
        if station == 'test':
            await message.reply('Вы уже проходите тест!')
        elif station in ('quiz', 'exam'):
            await message.reply('Завершите игру что бы начать этот режим!')
        return

    await start_test_func(bot, user)

@dp.message(F.text == 'STOP')
async def stop_game(message: types.Message):
    user = message.from_user.id
    
    user_station = await get_station_record(user)
    
    if user_station is None:
        return
    station = user_station['station']
    
    if message.text == 'STOP':
        if station == 'quiz':
            await delete_station_record(user)
            await message.answer('Привет! Я бот на aiogram!', reply_markup=menu)
        elif station in ('test', 'exam'):
            await message.answer('Вы уверены? Тогда результат обнулиться!', reply_markup=stop_continue_keyboard)
        return


@dp.message(F.text)
async def all_text(message: types.Message):
    user = message.from_user.id
    user_station = await get_station_record(user)
    
    if user_station is None:
        return

    station = user_station['station']

    if station == 'quiz':
        word_translation = await get_word_by_id(user_station['word_id'], table='words')
    elif station in ('test', 'exam'):
        word_translation = await get_word_by_id(user_station['word_id'], table='words_test')

    correct_answer = user_station['correct_answer']
    incorrect_answer = user_station['incorrect_answer']

    if message.text == word_translation['translation']:
        await message.reply(f'<b>Правильно!</b>', parse_mode=ParseMode.HTML)
        correct_answer += 1
    else:
        await message.reply(f'<b>Не правильно!</b> Правильный ответ: <b>{word_translation['translation']}</b>', parse_mode=ParseMode.HTML)
        incorrect_answer += 1
    
    if station == 'quiz':
        await start_quiz_func(bot, user)
    elif station in ('test', 'exam'):
        await update_station_record(user, station=station, correct_answer=correct_answer, incorrect_answer=incorrect_answer)
        if station == 'test':
            await start_test_func(bot, user)
        elif station == 'exam':
            await start_exam_func(bot, user)

@dp.callback_query(lambda c: c.data == 'start_exam')
async def start_exam_callback(callback: types.CallbackQuery):
    user = callback.from_user.id
    user_data = await get_user_record(user)
    user_station = await get_station_record(user)

    await bot.delete_message(
        chat_id=user,
        message_id=callback.message.message_id,
        request_timeout=1
    )


    if user_data['can_start_exam'] == False:
        return
    if user_station is not None:
        station = user_station['station']
        if station == 'exam':
            await bot.send_message(user, 'Вы уже проходите эказамен!')
        elif station in ('test', 'quiz'):
            await bot.send_message(user, 'Завершите игру что бы начать этот режим!')
        return

    await start_exam_func(bot, user)


@dp.callback_query(lambda c: c.data == 'stop')
async def stop_test_exam(callback: types.CallbackQuery):
    user = callback.from_user.id
    user_station = await get_station_record(user)

    await bot.delete_message(
        chat_id=user,
        message_id=callback.message.message_id,
    )    
    await delete_station_record(user)
    
    await bot.send_message(user, 'Привет! Я бот на aiogram!', reply_markup=menu)

    
@dp.callback_query(lambda c: c.data == 'continuе')
async def continue_test_exam(callback: types.CallbackQuery):
    user = callback.from_user.id
    await bot.delete_message(
        chat_id=user,
        message_id=callback.message.message_id
    )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main())