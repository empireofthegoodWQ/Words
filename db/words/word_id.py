import aiomysql
import asyncio
from db.db_config import db_config


async def get_word_id(
    search_term: str,
    table: str,  # "words" or "test"
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
) -> int | None:
    """
    Асинхронно находит ID слова в указанной таблице по слову или переводу.

    Args:
        search_term: Слово или перевод для поиска.
        table: "words" или "test", указывающая таблицу для поиска (words или words_test).
        db_host: Хост базы данных (по умолчанию из db_config).
        db_port: Порт базы данных (по умолчанию из db_config).
        db_user: Имя пользователя базы данных (по умолчанию из db_config).
        db_password: Пароль пользователя базы данных (по умолчанию из db_config).
        db_name: Имя базы данных (по умолчанию из db_config).

    Returns:
        ID слова, если найдено, иначе None.
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
            sql = f"""
                SELECT id FROM `{table}`
                WHERE word = %s OR translation = %s
            """
            val = (search_term, search_term)

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)
            result = await cur.fetchone()

            if result:
                return result['id']  # Возвращаем ID, если найдено
            else:
                return None  # Возвращаем None, если не найдено

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return None  # Return None on error
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None  # Return None on error
    finally:
        if conn:
            conn.close()