import sqlite3

# Подключаемся к БД напрямую
conn = sqlite3.connect('ssanych.db')
cursor = conn.cursor()

# Добавляем колонки
columns = [
    ("description", "TEXT"),
    ("photo", "VARCHAR(500)"),
    ("working_hours", "VARCHAR(100) DEFAULT '24/7'"),
    ("has_soap", "BOOLEAN DEFAULT 1"),
    ("has_paper", "BOOLEAN DEFAULT 1"),
    ("has_dryer", "BOOLEAN DEFAULT 0"),
    ("has_mirror", "BOOLEAN DEFAULT 1")
]

for col_name, col_type in columns:
    try:
        cursor.execute(f"ALTER TABLE toilet ADD COLUMN {col_name} {col_type}")
        print(f"Добавлена колонка: {col_name}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"Колонка {col_name} уже существует")
        else:
            print(f"Ошибка: {e}")

# Обновляем данные
cursor.execute("UPDATE toilet SET description = 'Уютная кофейня с чистым туалетом', working_hours = '08:00-22:00', has_dryer = 1 WHERE name LIKE '%Кофейня%'")
cursor.execute("UPDATE toilet SET description = 'Современный торговый центр', working_hours = '10:00-22:00', has_dryer = 1 WHERE name LIKE '%ТЦ%'")
cursor.execute("UPDATE toilet SET description = 'Ресторан с видом на море', working_hours = '09:00-23:00' WHERE name LIKE '%Ресторан%'")

conn.commit()
conn.close()

print("База данных успешно обновлена!")