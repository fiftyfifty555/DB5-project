import psycopg2
from faker import Faker
from random import randint, choice, random
from datetime import datetime

# Устанавливаем соединение с базой данных
conn = psycopg2.connect(
    dbname="lab3_v2",
    user="postgres",
    password="Vk280205",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Создаем объект Faker
fake = Faker()

# Функция для ограничения длины строк
def truncate_string(string, max_length):
    return string[:max_length] if string and len(string) > max_length else string

# Создаем массив 500 имен курсов
courses = [truncate_string(fake.sentence(nb_words=3), 50) for _ in range(500)]


# 1 шаг
# Функция для вставки данных в таблицу Пользователь
def insert_users(count):
    for _ in range(count):
        # Цикл для генерации уникального логина
        while True:
            логин = truncate_string(fake.user_name(), 20)  # Ограничение VARCHAR(20)
            cursor.execute("SELECT COUNT(*) FROM Пользователь WHERE логин = %s", (логин,))
            if cursor.fetchone()[0] == 0:  # Если логин не найден, выходим из цикла
                break

        # Цикл для генерации уникального email
        while True:
            email = truncate_string(fake.email(), 20)  # Ограничение VARCHAR(20)
            cursor.execute("SELECT COUNT(*) FROM Пользователь WHERE email = %s", (email,))
            if cursor.fetchone()[0] == 0:  # Если email не найден, выходим из цикла
                break

        дата_регистрации = fake.date_between(start_date='-2y', end_date='today')
        пароль = truncate_string(fake.password(length=10), 10)  # Ограничение VARCHAR(10)

        # Значения для строковых полей "сертификаты" и "избранное" выбираются из массива courses
        сертификаты = choice(courses) if random() < 0.3 else None
        избранное = choice(courses) if random() < 0.5 else None
        creator = choice([True, False])

        cursor.execute("""
            INSERT INTO Пользователь (логин, email, дата_регистрации, пароль, сертификаты, избранное, creator)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (логин, email, дата_регистрации, пароль, сертификаты, избранное, creator))

    conn.commit()

# 2 шаг

# Функция для вставки данных в таблицу Курс
def insert_courses(count):
    for _ in range(count):
        стоимость = round(random() * 1000, 2)
        авторы = truncate_string(fake.name(), 100)  # Ограничение TEXT
        описание = truncate_string(fake.text(max_nb_chars=200), 200)  # Ограничение TEXT
        название = choice(courses)  # Выбор случайного названия из массива courses
        cursor.execute("""
            INSERT INTO Курс (стоимость, авторы, описание, название)
            VALUES (%s, %s, %s, %s)
        """, (стоимость, авторы, описание, название))
    conn.commit()

# Функция для вставки данных в таблицу user_course
def insert_user_course(count):
    # Получение всех user_id из таблицы Пользователь
    cursor.execute("SELECT user_id FROM Пользователь")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Получение всех course_id из таблицы Курс
    cursor.execute("SELECT course_id FROM Курс")
    course_ids = [row[0] for row in cursor.fetchall()]
    
    # Проверка, чтобы списки user_ids и course_ids не были пустыми
    if not user_ids or not course_ids:
        raise ValueError("Списки user_ids или course_ids пусты. Проверьте наличие данных в таблицах Пользователь и Курс.")

    # Выполнение вставки данных в таблицу user_course
    for _ in range(count):
        user_id = choice(user_ids)  # Случайный выбор user_id
        course_id = choice(course_ids)  # Случайный выбор course_id
        
        cursor.execute("""
            INSERT INTO user_course (user_id, course_id)
            VALUES (%s, %s)
        """, (user_id, course_id))
    
    # Сохранение изменений в базе данных
    conn.commit()

# 3 шаг
    # Функция для вставки данных в таблицу Достижения
def insert_achievements(count):
    for _ in range(count):
        требования = truncate_string(fake.text(max_nb_chars=100), 100)  # Ограничение TEXT
        cursor.execute("""
            INSERT INTO Достижения (требования)
            VALUES (%s)
        """, (требования,))
    conn.commit()

    # Функция для вставки данных в таблицу Акция
def insert_promotions(count):
    for _ in range(count):
        promocode = truncate_string(fake.lexify(text="?????").upper(), 10)  # Ограничение VARCHAR(10)
        срок_действия = fake.date_between(start_date='today', end_date='+1y')
        cursor.execute("""
            INSERT INTO Акция (promocode, срок_действия)
            VALUES (%s, %s)
        """, (promocode, срок_действия))
    conn.commit()

    # Функция для вставки данных в таблицу Вложения
def insert_attachments(count):
    formats = ['pdf', 'docx', 'xlsx', 'pptx', 'txt']
    for _ in range(count):
        название = truncate_string(fake.file_name(extension=None), 30)  # Ограничение VARCHAR(30)
        ссылка = truncate_string(fake.url(), 255)  # Ограничение TEXT
        формат = choice(formats)  # Ограничение VARCHAR(4)
        cursor.execute("""
            INSERT INTO Вложения (название, ссылка, формат)
            VALUES (%s, %s, %s)
        """, (название, ссылка, формат))
    conn.commit()

# 4 шаг
    # Функция для вставки данных в таблицу achievement_user
def insert_achievement_user(count):
    # Получение всех user_id из таблицы Пользователь
    cursor.execute("SELECT user_id FROM Пользователь")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Получение всех achievement_id из таблицы Достижения
    cursor.execute("SELECT achievement_id FROM Достижения")
    achievement_ids = [row[0] for row in cursor.fetchall()]

    # Проверка на наличие данных в таблицах Пользователь и Достижения
    if not user_ids or not achievement_ids:
        raise ValueError("Списки user_ids или achievement_ids пусты. Проверьте наличие данных в таблицах Пользователь и Достижения.")

    # Вставка данных в таблицу achievement_user
    for _ in range(count):
        user_id = choice(user_ids)  # Случайный выбор user_id
        achievement_id = choice(achievement_ids)  # Случайный выбор achievement_id
        дата_достижения = fake.date_between(start_date='-2y', end_date='today')  # Генерация случайной даты

        cursor.execute("""
            INSERT INTO achievement_user (achievement_id, user_id)
            VALUES (%s, %s)
        """, (achievement_id, user_id))
    
    # Сохранение изменений в базе данных
    conn.commit()

# Функция для вставки данных в таблицу promo_user
def insert_promo_user(count):
    # Получение всех user_id из таблицы Пользователь
    cursor.execute("SELECT user_id FROM Пользователь")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Получение всех promo_id из таблицы Акция
    cursor.execute("SELECT promo_id FROM Акция")
    promo_ids = [row[0] for row in cursor.fetchall()]

    # Проверка на наличие данных в таблицах Пользователь и Акция
    if not user_ids or not promo_ids:
        raise ValueError("Списки user_ids или promo_ids пусты. Проверьте наличие данных в таблицах Пользователь и Акция.")

    # Вставка данных в таблицу promo_user
    for _ in range(count):
        user_id = choice(user_ids)  # Случайный выбор user_id
        promo_id = choice(promo_ids)  # Случайный выбор promo_id

        cursor.execute("""
            INSERT INTO promo_user (promo_id, user_id)
            VALUES (%s, %s)
        """, (promo_id, user_id))

    # Сохранение изменений в базе данных
    conn.commit()

# 5 шаг

# Функция для вставки данных в таблицу Оценка
def insert_grades(count):
    # Получение всех user_id из таблицы Пользователь
    cursor.execute("SELECT user_id FROM Пользователь")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Получение всех course_id из таблицы Курс
    cursor.execute("SELECT course_id FROM Курс")
    course_ids = [row[0] for row in cursor.fetchall()]

    # Проверка на наличие данных в таблицах Пользователь и Курс
    if not user_ids or not course_ids:
        raise ValueError("Списки user_ids или course_ids пусты. Проверьте наличие данных в таблицах Пользователь и Курс.")

    # Вставка данных в таблицу Оценка
    for _ in range(count):
        user_id = choice(user_ids)  # Случайный выбор user_id
        course_id = choice(course_ids)  # Случайный выбор course_id
        оценка = randint(1, 5)  # Случайная оценка от 1 до 5
        дата_оценки = fake.date_between(start_date='-1y', end_date='today')  # Дата за последний год
        отзыв = fake.text(max_nb_chars=200)  # Генерация случайного отзыва (до 200 символов)

        # Выполнение SQL-запроса для вставки данных
        cursor.execute("""
            INSERT INTO Оценка (user_id, course_id, значение, дата, отзыв)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, course_id, оценка, дата_оценки, отзыв))

    # Сохранение изменений в базе данных
    conn.commit()

# 6 шаг

# Функция для вставки данных в таблицу Урок
def insert_lessons(count):
    # Получение всех course_id из таблицы Курс
    cursor.execute("SELECT course_id FROM Курс")
    course_ids = [row[0] for row in cursor.fetchall()]

    # Проверка на наличие записей в таблице Курс
    if not course_ids:
        raise ValueError("Таблица 'Курс' пуста. Добавьте курсы перед добавлением уроков.")

    # Генерация уроков и вставка в таблицу Урок
    for _ in range(count):
        course_id = choice(course_ids)  # Случайный выбор course_id
        название = truncate_string(fake.sentence(nb_words=4), 50)  # Ограничение строки до 50 символов

        # Вставка данных в таблицу Урок
        cursor.execute("""
            INSERT INTO Урок (course_id, название)
            VALUES (%s, %s)
        """, (course_id, название))

    # Сохранение изменений в базе данных
    conn.commit()

# 7 шаг

# Функция для вставки данных в таблицу Комментарий
def insert_comments(count):
    # Получение всех user_id из таблицы Пользователь
    cursor.execute("SELECT user_id FROM Пользователь")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Проверка: есть ли пользователи в таблице Пользователь
    if not user_ids:
        raise ValueError("Таблица 'Пользователь' пуста. Добавьте пользователей перед добавлением комментариев.")

    # Получение всех lesson_id из таблицы Урок
    cursor.execute("SELECT lesson_id FROM Урок")
    lesson_ids = [row[0] for row in cursor.fetchall()]

    # Проверка: есть ли уроки в таблице Урок
    if not lesson_ids:
        raise ValueError("Таблица 'Урок' пуста. Добавьте уроки перед добавлением комментариев.")
    
    # Генерация комментариев и вставка в таблицу Комментарий
    for _ in range(count):
        user_id = choice(user_ids)  # Случайный выбор user_id
        lesson_id = choice(lesson_ids)  # Случайный выбор lesson_id
        текст = fake.text(max_nb_chars=200)  # Генерация текста комментария (до 200 символов)
        дата_комментария = fake.date_between(start_date='-1y', end_date='today')  # Дата в диапазоне последних 12 месяцев

        # Вставка данных в таблицу Комментарий
        cursor.execute("""
            INSERT INTO Комментарий (user_id, lesson_id, текст, дата)
            VALUES (%s, %s, %s, %s)
        """, (user_id, lesson_id, текст, дата_комментария))
    
    # Сохранение всех изменений
    conn.commit()

# 8  шаг

# Функция для вставки данных в таблицу Степ
def insert_steps(count):
    # Получение всех lesson_id из таблицы Урок
    cursor.execute("SELECT lesson_id FROM Урок")
    lesson_ids = [row[0] for row in cursor.fetchall()]

    # Проверка: есть ли уроки в таблице Урок
    if not lesson_ids:
        raise ValueError("Таблица 'Урок' пуста. Добавьте уроки перед добавлением степов.")
    
    # Генерация данных и добавление в таблицу Степ
    for _ in range(count):
        lesson_id = choice(lesson_ids)  # Случайный выбор lesson_id
        название = truncate_string(fake.sentence(nb_words=5), 50)  # Ограничение для VARCHAR(50)
        текст = truncate_string(fake.text(max_nb_chars=300), 300)  # Ограничение для TEXT
        
        # Вставка данных в таблицу Степ
        cursor.execute("""
            INSERT INTO Степ (lesson_id, название, текст)
            VALUES (%s, %s, %s)
        """, (lesson_id, название, текст))
    
    # Сохранение всех изменений
    conn.commit()

# 9 шаг

# Функция для вставки данных в таблицу attachment_step
def insert_attachment_step(count):
    # Получение всех step_id из таблицы Степ
    cursor.execute("SELECT step_id FROM Степ")
    step_ids = [row[0] for row in cursor.fetchall()]

    # Получение всех attachment_id из таблицы Вложения
    cursor.execute("SELECT attachment_id FROM Вложения")
    attachment_ids = [row[0] for row in cursor.fetchall()]

    # Проверка: есть ли данные в необходимых таблицах
    if not step_ids:
        raise ValueError("Таблица 'Степ' пуста. Добавьте шаги перед добавлением данных в 'Attachment_step'.")
    if not attachment_ids:
        raise ValueError("Таблица 'Вложения' пуста. Добавьте вложения перед добавлением данных в 'Attachment_step'.")

    # Генерация и вставка данных
    for _ in range(count):
        step_id = choice(step_ids)  # Случайный выбор step_id
        attachment_id = choice(attachment_ids)  # Случайный выбор attachment_id

        # Вставка данных в таблицу Attachment_step
        cursor.execute("""
            INSERT INTO Attachment_step (step_id, attachment_id)
            VALUES (%s, %s)
        """, (step_id, attachment_id))
    
    # Сохранение изменений в БД
    conn.commit()

try:
    insert_users(10000)
    insert_courses(500)
    insert_user_course(3500)
    insert_achievements(150)
    insert_promotions(10)
    insert_attachments(3100)
    insert_achievement_user(1750)
    insert_promo_user(2000)
    insert_grades(6530)
    insert_lessons(5000)
    insert_comments(20000)
    insert_steps(40000)
    insert_attachment_step(15000)
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()