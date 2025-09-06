from db.user.get_user_record import get_user_record
from db.words.words_by_lesson import get_words_by_lesson

async def get_lesson_func(bot, user):
    user_data = await get_user_record(user)
    words = await get_words_by_lesson(user_data['lesson'])

    text = ''

    for key, value in words.items():
        text = text + f'{key} - {value}\n'
    await bot.send_message(user, text)
