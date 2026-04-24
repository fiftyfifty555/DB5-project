-- Таблица Пользователь
CREATE TABLE Пользователь (
    user_id SERIAL PRIMARY KEY,
    логин VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(20) UNIQUE NOT NULL,
    дата_регистрации DATE NOT NULL,
    пароль VARCHAR(10) NOT NULL,
    сертификаты TEXT,
    избранное TEXT,
    creator BOOLEAN DEFAULT FALSE
);

-- Таблица Достижения
CREATE TABLE Достижения (
    achievement_id SERIAL PRIMARY KEY,
    требования TEXT
);

-- Таблица Акция
CREATE TABLE Акция (
    promo_id SERIAL PRIMARY KEY,
    promocode VARCHAR(10) NOT NULL,
    срок_действия DATE NOT NULL
);

-- Таблица promo_user (связь между Акцией и Пользователем)
CREATE TABLE promo_user (
    promo_user_id SERIAL PRIMARY KEY,
    promo_id INT REFERENCES Акция(promo_id) ON DELETE CASCADE,
    user_id INT REFERENCES Пользователь(user_id) ON DELETE CASCADE
);

-- Таблица achievement_user (связь между Достижениями и Пользователем)
CREATE TABLE achievement_user (
    achievement_user_id SERIAL PRIMARY KEY,
    achievement_id INT REFERENCES Достижения(achievement_id) ON DELETE CASCADE,
    user_id INT REFERENCES Пользователь(user_id) ON DELETE CASCADE
);

-- Таблица Курс
CREATE TABLE Курс (
    course_id SERIAL PRIMARY KEY,
    стоимость DECIMAL(10, 2),
    авторы TEXT,
    описание TEXT,
    название VARCHAR(50) NOT NULL
);

-- Таблица Урок
CREATE TABLE Урок (
    lesson_id SERIAL PRIMARY KEY,
    course_id INT REFERENCES Курс(course_id) ON DELETE CASCADE,
    название VARCHAR(50)
);

-- Таблица Степ
CREATE TABLE Степ (
    step_id SERIAL PRIMARY KEY,
    lesson_id INT REFERENCES Урок(lesson_id) ON DELETE CASCADE,
    название VARCHAR(50),
    текст TEXT
);

-- Таблица Вложения
CREATE TABLE Вложения (
    attachment_id SERIAL PRIMARY KEY,
    название VARCHAR(30),
    ссылка TEXT,
    формат VARCHAR(4)
);

-- Таблица Attachment_step (связь между Степ и Вложения)
CREATE TABLE Attachment_step (
    attachment_step_id SERIAL PRIMARY KEY,
    step_id INT REFERENCES Степ(step_id) ON DELETE CASCADE,
    attachment_id INT REFERENCES Вложения(attachment_id) ON DELETE CASCADE
);

-- Таблица Оценка
CREATE TABLE Оценка (
    grade_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Пользователь(user_id) ON DELETE CASCADE,
    course_id INT REFERENCES Курс(course_id) ON DELETE CASCADE,
    значение INT CHECK (значение >= 1 AND значение <= 5),
    дата DATE,
    отзыв TEXT
);

-- Таблица user_course (связь между Пользователем и Курсом)
CREATE TABLE user_course (
    user_course_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Пользователь(user_id) ON DELETE CASCADE,
    course_id INT REFERENCES Курс(course_id) ON DELETE CASCADE
);

-- Таблица Комментарий
CREATE TABLE Комментарий (
    comment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Пользователь(user_id) ON DELETE CASCADE,
    lesson_id INT REFERENCES Урок(lesson_id) ON DELETE CASCADE,
    текст TEXT,
    дата TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
