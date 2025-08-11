import aiomysql
import asyncio
from db.db_config import db_config

async def add_user(
    telegram_id: int,
    level: int = 0,  # Значение по умолчанию
    lesson: int = 1,   # Значение по умолчанию
    can_start_test: bool = False,  # Значение по умолчанию
    can_start_exam: bool = False,   # Значение по умолчанию
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
) -> bool:
    """
    Асинхронно добавляет нового пользователя в базу данных MySQL.

    Args:
        telegram_id: Telegram ID пользователя.
        db_host: Хост базы данных.
        db_port: Порт базы данных.
        db_user: Имя пользователя базы данных.
        db_password: Пароль пользователя базы данных.
        db_name: Имя базы данных.
        level: Начальный уровень пользователя (по умолчанию 1).
        lesson: Начальный урок пользователя (по умолчанию 1).
        can_start_test: Флаг, разрешающий начинать тест (по умолчанию False).
        can_start_exam: Флаг, разрешающий начинать экзамен (по умолчанию False).

    Returns:
        True, если пользователь успешно добавлен, иначе False.
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
            # Проверяем, существует ли пользователь с таким telegram_id
            sql_check = "SELECT telegram_id FROM users WHERE telegram_id = %s"
            val_check = (telegram_id,)
            await cur.execute(sql_check, val_check)
            existing_user = await cur.fetchone()

            if existing_user:
                print(f"Пользователь с telegram_id {telegram_id} уже существует.")
                return False  # Пользователь уже существует

            # Формируем SQL запрос для добавления пользователя.
            sql = """
                INSERT INTO users (telegram_id, level, lesson, can_start_test, can_start_exam)
                VALUES (%s, %s, %s, %s, %s)
            """
            val = (telegram_id, level, lesson, can_start_test, can_start_exam)

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)
            await conn.commit()  # Подтверждаем изменения

            return True  # Пользователь успешно добавлен

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False
    finally:
        if conn:
            conn.close()
