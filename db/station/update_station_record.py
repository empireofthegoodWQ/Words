import aiomysql
from db.db_config import db_config

async def update_station_record(
    telegram_id: int,
    station: str = None,
    word_id: int = None,
    correct_answer: int = None,
    incorrect_answer: int = None,
    db_host: str = db_config[0],
    db_port: int = db_config[1],
    db_user: str = db_config[2],
    db_password: str = db_config[3],
    db_name: str = db_config[4],
) -> bool:
    """
    Асинхронно обновляет данные в таблице 'station' для заданной записи.  Обновляет только те поля,
    которые переданы в функцию (остальные остаются без изменений).

    Args:
        telegram_id: Telegram ID пользователя (для идентификации записи).
        station: Название станции (Если указано).
        word_id: ID слова (Новое значение если указано).
        correct_answer: Новое количество правильных ответов (Если указано).
        incorrect_answer: Новое количество неправильных ответов (Если указано).
        db_host: Хост базы данных (по умолчанию из db_config).
        db_port: Порт базы данных (по умолчанию из db_config).
        db_user: Имя пользователя базы данных (по умолчанию из db_config).
        db_password: Пароль пользователя базы данных (по умолчанию из db_config).
        db_name: Имя базы данных (по умолчанию из db_config).

    Returns:
        True, если данные успешно обновлены, иначе False.
    """
    try:
        async with aiomysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name,
            autocommit=True,
        ) as conn:
            async with conn.cursor() as cur:
                # Build the update query dynamically
                query = "UPDATE station SET "
                updates = []
                values = []

                if station is not None:
                    updates.append("station = %s")
                    values.append(station)
                if word_id is not None:
                    updates.append("word_id = %s")
                    values.append(word_id)
                if correct_answer is not None:
                    updates.append("correct_answer = %s")
                    values.append(correct_answer)
                if incorrect_answer is not None:
                    updates.append("incorrect_answer = %s")
                    values.append(incorrect_answer)

                if not updates:
                    # No updates provided, nothing to do
                    return True

                query += ", ".join(updates)
                query += " WHERE telegram_id = %s"
                values.append(telegram_id)

                await cur.execute(query, values)
                await conn.commit()

                return cur.rowcount > 0
    except aiomysql.MySQLError as e:  # Catch specific aiomysql errors
        print(f"MySQL error updating station data: {e}")
        return False
    except Exception as e:
        print(f"General error updating station data: {e}")
        return False
