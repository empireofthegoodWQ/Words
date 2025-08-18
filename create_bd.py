import asyncio
import aiomysql

async def create_tables_async(db_host, db_user, db_password, db_name):
    """
    Асинхронно создает базу данных DB_bot (если не существует) и таблицы station, users, words и words_test в базе данных MySQL.

    Args:
        db_host (str): Хост базы данных (например, "localhost").
        db_user (str): Имя пользователя базы данных.
        db_password (str): Пароль пользователя базы данных.
        db_name (str): Имя базы данных, по умолчанию "DB_bot".
    """
    conn = None
    try:
        # Подключение к MySQL без указания базы данных (для создания БД)
        conn = await aiomysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db='',  # Подключаемся без указания конкретной базы данных
            loop=asyncio.get_event_loop()
        )

        async with conn.cursor() as cur:
            try:
                # Создаем базу данных
                await cur.execute(f"CREATE DATABASE {db_name}")
                print(f"База данных '{db_name}' успешно создана.")
            except aiomysql.MySQLError as e:
                if e.args[0] == 1007:  # Check for 'database exists' error code
                    print(f"База данных '{db_name}' уже существует.")
                else:
                    raise  # Re-raise the exception if it's not the 'database exists' error


        # Закрываем соединение и создаем новое, указав созданную базу данных
        conn.close()  # Закрываем соединение
        conn = await aiomysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name,  # Подключаемся к созданной базе данных
            loop=asyncio.get_event_loop()
        )

        async with conn.cursor() as cur:

            # SQL-запросы для создания таблиц
            create_users_table_query = """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                level INT,
                lesson INT,
                can_start_test BOOLEAN,  -- Используем BOOLEAN вместо TINYINT(1) для читабельности, но MySQL хранит его как TINYINT(1)
                can_start_exam BOOLEAN  -- Используем BOOLEAN вместо TINYINT(1) для читабельности, но MySQL хранит его как TINYINT(1)
            );
            """

            create_words_table_query = """
                CREATE TABLE words (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lesson INT,
                    word VARCHAR(40),
                    translation VARCHAR(40)
                );
            """

            create_words_test_table_query = """
                CREATE TABLE words_test (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lesson INT,
                    word TEXT,
                    translation TEXT
                );
            """

            create_station_table_query = """
                CREATE TABLE station (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    telegram_id BIGINT,
                    station VARCHAR(10),
                    word_id INT,
                    correct_answer INT,
                    incorrect_answer INT,
                    INDEX (word_id) -- Добавление индекса на поле word_id (создает внешний ключ, если необходимо)
                );
            """

            # Выполнение SQL-запросов асинхронно
            await cur.execute(create_users_table_query)
            await cur.execute(create_words_table_query)
            await cur.execute(create_words_test_table_query)
            await cur.execute(create_station_table_query)

            await conn.commit()
            print("Таблицы успешно созданы.")

    except aiomysql.MySQLError as err:
        print(f"Ошибка: {err}")
    finally:
        if conn:
            await conn.ensure_closed() # use ensure_closed instead of close
            print("Соединение с базой данных успешно закрыто.")

# Пример использования функции:
async def main():
    host = input("Enter the host address (default: localhost): ")
    db_host = host if host != "" else "localhost"
    # Или другой хост, если база данных не на локальной машине

    db_user = input("Username for database connection: ")  # Замените на ваше имя пользователя MySQL
    db_password = input("Password: ")  # Замените на ваш пароль MySQL

    name = input("Database name (default: DB_Bot): ")
    db_name = name if name != "" else "DB_Bot"

    await create_tables_async(db_host, db_user, db_password, db_name)

if __name__ == '__main__':
    asyncio.run(main())
