import aiomysql
import asyncio
from db.db_config import db_config

async def get_user_record(
    telegram_id: int,
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
) -> dict:
    """
    Асинхронно извлекает данные пользователя из базы данных MySQL.

    Args:
        telegram_id: Telegram ID пользователя.
        db_host: Хост базы данных.
        db_port: Порт базы данных.
        db_user: Имя пользователя базы данных.
        db_password: Пароль пользователя базы данных.
        db_name: Имя базы данных.

    Returns:
        Словарь с данными пользователя, если пользователь найден, иначе None.
    """
    conn = None  # Инициализируем conn вне try блока

    try:
        # Устанавливаем соединение с базой данных асинхронно.
        conn = await aiomysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name,
            loop=asyncio.get_event_loop(),
        )

        async with conn.cursor(aiomysql.DictCursor) as cur:  # Используем DictCursor для возврата словарей
            # Формируем SQL запрос для поиска пользователя по telegram_id.
            sql = "SELECT * FROM users WHERE telegram_id = %s"
            val = (telegram_id,)

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)

            # Получаем результат запроса.  fetchone() возвращает None, если ничего не найдено
            result = await cur.fetchone()

            # Возвращаем данные пользователя, если он найден.
            if result:
                return result
            else:
                return None

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        if conn:
            conn.close()
