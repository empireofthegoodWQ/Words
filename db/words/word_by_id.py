import aiomysql
import asyncio
from db.db_config import db_config

async def get_word_by_id(
    word_id: int,
    table: str,  # "words" or "words_test"
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
) -> dict | None:
    """
    Асинхронно получает слово из указанной таблицы (words или words_test) по его ID.

    Args:
        word_id: ID слова, которое нужно найти.
        table: "words" или "words_test" - имя таблицы, из которой нужно получить слово.
        db_host: Хост базы данных (по умолчанию из db_config).
        db_port: Порт базы данных (по умолчанию из db_config).
        db_user: Имя пользователя базы данных (по умолчанию из db_config).
        db_password: Пароль пользователя базы данных (по умолчанию из db_config).
        db_name: Имя базы данных (по умолчанию из db_config).

    Returns:
        Словарь с данными слова, если слово найдено, иначе None.
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
            sql = f"SELECT * FROM `{table}` WHERE id = %s"
            val = (word_id,)

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)
            result = await cur.fetchone()

            return result  # Возвращаем словарь с данными слова или None

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        if conn:
            conn.close()