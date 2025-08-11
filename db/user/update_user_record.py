import aiomysql
import asyncio
from db.db_config import db_config


async def update_user_record(
    telegram_id: int,
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
    **kwargs,  # Keyword arguments for fields to update
) -> bool:
    """
    Асинхронно обновляет заданные поля в таблице 'users' для пользователя с указанным telegram_id.

    Args:
        telegram_id: Telegram ID пользователя, которого нужно обновить.
        db_host: Хост базы данных (по умолчанию из db_config).
        db_port: Порт базы данных (по умолчанию из db_config).
        db_user: Имя пользователя базы данных (по умолчанию из db_config).
        db_password: Пароль пользователя базы данных (по умолчанию из db_config).
        db_name: Имя базы данных (по умолчанию из db_config).
        **kwargs: Ключевые аргументы, представляющие поля для обновления и их новые значения.
                 Например, `level=2, lesson=3`. Допустимые поля: 'level', 'lesson', 'can_start_test', 'can_start_exam'.

    Returns:
        True, если поля успешно обновлены, иначе False.
    """

    ALLOWED_FIELDS = ["level", "lesson", "can_start_test", "can_start_exam"]

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
            updates = []
            values = []

            for field, value in kwargs.items():
                if field in ALLOWED_FIELDS:
                    updates.append(f"`{field}` = %s")
                    values.append(value)
                else:
                    print(f"Недопустимое поле для обновления: {field}")
                    return False  # Нельзя обновлять, если есть недопустимое поле

            if not updates:
                print("Нет полей для обновления.")
                return True  # Ничего не нужно обновлять

            sql = f"""
                UPDATE users
                SET {', '.join(updates)}
                WHERE telegram_id = %s
            """
            values.append(telegram_id)  # Add telegram_id to the values
            val = tuple(values)

            # Выполняем запрос асинхронно.
            await cur.execute(sql, val)
            await conn.commit()

            return True  # Поля успешно обновлены

    except aiomysql.MySQLError as e:
        print(f"Ошибка базы данных: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False
    finally:
        if conn:
            conn.close()