import aiomysql
import asyncio
from db.db_config import db_config

async def get_station_record(
    telegram_id: int,
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
) -> dict | None:
    """
    Асинхронно получает данные станции из таблицы 'station' по telegram_id.

    Args:
        telegram_id: Telegram ID пользователя.
        db_host: Хост базы данных (по умолчанию из db_config).
        db_port: Порт базы данных (по умолчанию из db_config).
        db_user: Имя пользователя базы данных (по умолчанию из db_config).
        db_password: Пароль пользователя базы данных (по умолчанию из db_config).
        db_name: Имя базы данных (по умолчанию из db_config).

    Returns:
        Словарь с данными станции, если станция найдена, иначе None.
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
            sql = "SELECT * FROM station WHERE telegram_id = %s"
            val = (telegram_id,)  # Note the comma to make it a tuple

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)
            result = await cur.fetchone()

            return result  # Возвращаем словарь с данными станции или None

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        if conn:
            conn.close()
