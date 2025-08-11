import aiomysql
import asyncio
from db.db_config import db_config

async def add_station_record(
    telegram_id: int,
    station: str,
    word_id: int,
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
    correct_answer: int = 0,  # Значение по умолчанию
    incorrect_answer: int = 0   # Значение по умолчанию
) -> bool:
    """
    Асинхронно добавляет данные в таблицу 'station'.

    Args:
        telegram_id: Telegram ID пользователя.
        station: Название станции.
        word_id: ID слова.
        db_host: Хост базы данных.
        db_port: Порт базы данных.
        db_user: Имя пользователя базы данных.
        db_password: Пароль пользователя базы данных.
        db_name: Имя базы данных.
        correct_answer: Количество правильных ответов (по умолчанию 0).
        incorrect_answer: Количество неправильных ответов (по умолчанию 0).

    Returns:
        True, если данные успешно добавлены, иначе False.
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
        )

        async with conn.cursor() as cur:
            # Формируем SQL запрос для вставки данных.
            sql = """
                INSERT INTO station (telegram_id, station, word_id, correct_answer, incorrect_answer)
                VALUES (%s, %s, %s, %s, %s)
            """
            val = (telegram_id, station, word_id, correct_answer, incorrect_answer)

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)
            await conn.commit()  # Подтверждаем изменения

            return True  # Данные успешно добавлены

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False
    finally:
        if conn:
            conn.close()
