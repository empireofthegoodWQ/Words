import aiomysql
import asyncio
from db.db_config import db_config

async def get_words_test_by_lesson(
    lesson: int,
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
) -> dict:  # Возвращаем словарь
    """
    Асинхронно извлекает все слова из таблицы words_test для заданного урока и формирует словарь.

    Args:
        lesson: Номер урока.
        db_host: Хост базы данных (по умолчанию из db_config).
        db_port: Порт базы данных (по умолчанию из db_config).
        db_user: Имя пользователя базы данных (по умолчанию из db_config).
        db_password: Пароль пользователя базы данных (по умолчанию из db_config).
        db_name: Имя базы данных (по умолчанию из db_config).

    Returns:
        Словарь, где ключ - слово (word), а значение - словарь с 'id' и 'translation'.
        Пример: {'где промокашка': {'id': 14, 'translation': 'слово'}}.
        Возвращает пустой словарь, если ничего не найдено или произошла ошибка.
    """
    conn = None
    try:
        conn = await aiomysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name,
            loop=asyncio.get_event_loop(),
            cursorclass=aiomysql.DictCursor,  # Use DictCursor for dictionary results
        )

        async with conn.cursor() as cur:
            # Формируем SQL запрос для выборки данных.
            sql = "SELECT id, word, translation FROM words_test WHERE lesson = %s"
            val = (lesson,)

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)
            results = await cur.fetchall()

            # Формируем словарь в нужном формате
            word_dict = {}
            for row in results:
                word_dict[row['word']] = row['translation']

            return word_dict

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return {}  # Return an empty dictionary on error
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}  # Return an empty dictionary on error
    finally:
        if conn:
            conn.close()


