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
                await cur.execute(f"CREATE DATABASE {db_name}")
                print(f"База данных '{db_name}' успешно создана.")
            except aiomysql.MySQLError as e:
                if e.args[0] == 1007:  # Check for 'database exists' error code
                    print(f"База данных '{db_name}' уже существует.")
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
            create_users_table_query = """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                level INT,
                lesson INT,
                can_start_test BOOLEAN,
                can_start_exam BOOLEAN
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
                    INDEX (word_id)
                );
            """

            # Выполнение SQL-запросов асинхронно
            await cur.execute(create_users_table_query)
            await cur.execute(create_words_table_query)
            await cur.execute(create_words_test_table_query)
            await cur.execute(create_station_table_query)

            # Добавляем записи в таблицу words
            words_data = [
                (1, 'доска', 'لَوْحٌ'),
                (1, 'чернильница', 'مِحْبَرَةٌ'),
                (2, 'полотенце', 'نَشَّافَةٌ'),
                (2, 'линейка', 'مِسْطَرَةٌ'),
                (3, 'это', 'هَٰذَا'),
                (3, 'где?', 'أَيْنَ'),
                (4, 'дай', 'هَاتِ'),
                (4, 'книга', 'كِتَابٌ'),
                (5, 'карандаш', 'قَلَمٌ'),
                (5, 'брошюра', 'كُرَّاسٌ'),
                (6, 'листок', 'وَرَقٌ'),
                (6, 'перо', 'رِيشَةٌ'),
                (7, 'возьми', 'خُذْ'),
                (7, 'что?', 'مَا'),
                (8, 'где ключ?', 'أَيْنَ الْمِفْتَاحُ؟'),
                (8, 'где ключ?', 'أَيْنَ الْمِفْتَاحُ؟')
            ]
            
            await cur.executemany(
                "INSERT INTO words (lesson, word, translation) VALUES (%s, %s, %s)",
                words_data
            )

            # Добавляем записи в таблицу words_test
            words_test_data = [
                (1, 'где доска?', 'أَيْنَ لَوْحٌ؟'),
                (1, 'ты книга?', 'أَأَنْتَ كِتَابٌ؟'),
                (2, 'кто это?', 'مَنْ هَذَا؟'),
                (2, 'я учитель', 'أَنَا مُدَرِّسٌ'),
                (3, 'почему нет?', 'لِمَاذَا لَا؟'),
                (3, 'до свидания', 'إِلَى اللِّقَاءِ'),
                (4, 'большое спасибо', 'شُكْرًا جَزِيلًا'),
                (4, 'пожалуйста', 'مِنْ فَضْلِكَ'),
                (5, 'сколько стоит?', 'كَمْ هَذَا؟'),
                (5, 'это дорого', 'هَذَا غَالِي'),
                (6, 'как дела?', 'كَيْفَ حَالُكَ؟'),
                (6, 'все хорошо', 'بِخَيْرٍ'),
                (7, 'который час?', 'كَمِ السَّاعَةُ؟'),
                (7, 'семь часов', 'السَّاعَةُ سَابِعَةٌ'),
                (8, 'где ключ?', 'أَيْنَ الْمِفْتَاحُ؟'),
                (8, 'я устал', 'أَنَا مُتْعَبٌ')
            ]
            
            await cur.executemany(
                "INSERT INTO words_test (lesson, word, translation) VALUES (%s, %s, %s)",
                words_test_data
            )

            await conn.commit()
            print("Таблицы успешно созданы и заполнены данными.")
    except aiomysql.MySQLError as err:
        print(f"Ошибка: {err}")
    finally:
        if conn:
            await conn.ensure_closed()
            print("Соединение с базой данных успешно закрыто.")

async def main():
    host = input("Enter the host address (default: localhost): ")
    db_host = host if host != "" else "localhost"

    db_user = input("Username for database connection: ")
    db_password = input("Password: ")

    name = input("Database name (default: DB_Bot): ")
    db_name = name if name != "" else "DB_Bot"

    await create_tables_async(db_host, db_user, db_password, db_name)

if __name__ == '__main__':
    asyncio.run(main())
