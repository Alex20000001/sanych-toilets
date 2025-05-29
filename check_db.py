import sqlite3
import os

db_path = 'ssanych.db'

# Проверяем существование файла
if not os.path.exists(db_path):
    print(f"❌ База данных {db_path} не найдена!")
else:
    print(f"✓ База данных {db_path} существует")
    print(f"  Размер: {os.path.getsize(db_path)} байт")

# Подключаемся к базе
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    
    # Получаем список всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nТаблицы в базе данных:")
    for table in tables:
        table_name = table[0]
        print(f"\n📋 Таблица: {table_name}")
        
        # Получаем структуру каждой таблицы
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        if columns:
            print("  Колонки:")
            for col in columns:
                print(f"    - {col[1]} ({col[2]})")
        else:
            print("  ❌ Нет колонок или таблица пустая")
        
        # Считаем записи
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  Записей: {count}")

print("\nГотово!")
