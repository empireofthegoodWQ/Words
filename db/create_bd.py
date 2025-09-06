import asyncio
import aiomysql

async def create_tables_async(db_host, db_user, db_password, db_name):
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
                await cur.execute(f'CREATE DATABASE {db_name}')
                print(f'База данных "{db_name}" успешно создана.')
            except aiomysql.MySQLError as e:
                if e.args[0] == 1007:  # Check for 'database exists' error code
                    print(f'База данных "{db_name}" уже существует.')
                    return
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
            create_users_table_query = '''
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                level INT,
                lesson INT,
                can_start_test BOOLEAN,
                can_start_exam BOOLEAN
            );
            '''

            create_words_table_query = '''
                CREATE TABLE words (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lesson INT,
                    word VARCHAR(40),
                    translation VARCHAR(40)
                );
            '''

            create_words_test_table_query = '''
                CREATE TABLE words_test (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lesson INT,
                    word TEXT,
                    translation TEXT
                );
            '''

            create_station_table_query = '''
                CREATE TABLE station (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    telegram_id BIGINT,
                    station VARCHAR(10),
                    word_id INT,
                    correct_answer INT,
                    incorrect_answer INT,
                    INDEX (word_id)
                );
            '''

            # Выполнение SQL-запросов асинхронно
            await cur.execute(create_users_table_query)
            await cur.execute(create_words_table_query)
            await cur.execute(create_words_test_table_query)
            await cur.execute(create_station_table_query)

            # Добавляем записи в таблицу words
            words_data = [
                (1, 'Стол', 'Table'),
                (1, 'Стул', 'Chair'),
                (2, 'Книга', 'Book'),
                (2, 'Ручка', 'Pen'),
                (3, 'Это', 'This'),
                (3, 'Где?', 'Where?'),
                (4, 'Покажи', 'Show'),
                (4, 'Словарь', 'Dictionary'),
                (5, 'Тетрадь', 'Notebook'),
                (5, 'Карандаш', 'Pencil'),
                (6, 'Бумага', 'Paper'),
                (6, 'Доска', 'Board'),
                (7, 'Возьми', 'Take'),
                (7, 'Что?', 'What?'),
                (8, 'Где телефон?', 'Where is the phone?'),
                (8, 'Где телефон?', 'Where is the phone?')
            ]

            
            await cur.executemany(
                'INSERT INTO words (lesson, word, translation) VALUES (%s, %s, %s)',
                words_data
            )

            # Добавляем записи в таблицу words_test
            words_test_data = [
                (1, 'Где мел?', 'Where is the chalk?'),
                (1, 'Ты студент?', 'Are you a student?'),
                (2, 'Кто здесь?', 'Who is here?'),
                (2, 'Я врач', 'I am a doctor'),
                (3, 'Зачем?', 'Why?'),
                (3, 'Пока!', 'Goodbye!'),
                (4, 'Большое спасибо!', 'Thanks a lot!'),
                (4, 'Не за что', "You're welcome"),
                (5, 'Сколько стоит?', 'How much is it?'),
                (5, 'Это дороговато', 'That\'s pricey'),
                (6, 'Как жизнь?', 'How\'s life?'),
                (6, 'Все отлично', 'Everything is great'),
                (7, 'Который час?', 'What time is it?'),
                (7, 'Семь часов ровно', "It's seven o'clock sharp"),
                (8, 'Где ручка?', 'Where is the pen?'),
                (8, 'Я утомлен', 'I am weary')
            ]

            
            await cur.executemany(
                'INSERT INTO words_test (lesson, word, translation) VALUES (%s, %s, %s)',
                words_test_data
            )

            await conn.commit()
            print('Таблицы успешно созданы и заполнены данными.')
    except aiomysql.MySQLError as err:
        print(f'Ошибка: {err}')
    finally:
        if conn:
            await conn.ensure_closed()
            print('Соединение с базой данных успешно закрыто.')

async def main():
    host = input('Enter the host address (default: localhost): ')
    db_host = host if host != '' else 'localhost'

    db_user = input('Username for database connection (default: user): ')
    db_user = db_user if db_user != '' else 'user' 
    
    db_password = input('Password (default: 1234): ')
    db_password = db_password if db_password != '' else '1234' 

    with open('db/db_config.py', 'w') as file:
        file.write(f"db_config = ('localhost', 3306, '{db_user}', '{db_password}', 'DB_Bot')")

    name = input('Database name (default: DB_Bot): ')
    db_name = name if name != '' else 'DB_Bot'

    await create_tables_async(db_host, db_user, db_password, db_name)

if __name__ == '__main__':
    asyncio.run(main())
