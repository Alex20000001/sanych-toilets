from app import app, db
from sqlalchemy import text
import sqlite3

def get_table_columns(table_name):
    """Получить список колонок в таблице"""
    with sqlite3.connect('ssanych.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        return [column[1] for column in cursor.fetchall()]

with app.app_context():
    print("Начинаем обновление базы данных...")
    
    # Получаем текущие колонки в таблице toilet
    existing_columns = get_table_columns('toilet')
    print(f"Существующие колонки в таблице toilet: {existing_columns}")
    
    # Список новых колонок для добавления
    new_columns = [
        ('description', 'TEXT', None),
        ('photo', 'VARCHAR(500)', None),
        ('working_hours', 'VARCHAR(100)', "'24/7'"),
        ('has_soap', 'BOOLEAN', '1'),
        ('has_paper', 'BOOLEAN', '1'),
        ('has_dryer', 'BOOLEAN', '0'),
        ('has_mirror', 'BOOLEAN', '1')
    ]
    
    # Добавляем недостающие колонки
    with db.engine.connect() as conn:
        for column_name, column_type, default_value in new_columns:
            if column_name not in existing_columns:
                if default_value:
                    sql = f"ALTER TABLE toilet ADD COLUMN {column_name} {column_type} DEFAULT {default_value}"
                else:
                    sql = f"ALTER TABLE toilet ADD COLUMN {column_name} {column_type}"
                
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"✓ Добавлена колонка: {column_name}")
                except Exception as e:
                    print(f"✗ Ошибка при добавлении колонки {column_name}: {e}")
            else:
                print(f"- Колонка {column_name} уже существует")
    
    # Проверяем результат
    updated_columns = get_table_columns('toilet')
    print(f"\nКолонки после обновления: {updated_columns}")
    
    # Добавляем тестовые данные, если туалетов нет
    from app import Toilet, User
    
    if Toilet.query.count() == 0:
        business_user = User.query.filter_by(email='business@test.com').first()
        if business_user:
            test_toilets = [
                {
                    'name': 'Кофейня "Аромат"',
                    'address': 'ул. Ленина, 15',
                    'latitude': 43.5858,
                    'longitude': 39.7203,
                    'price': 50.0,
                    'rating': 4.8,
                    'is_accessible': True,
                    'description': 'Уютная кофейня с чистым туалетом',
                    'working_hours': '08:00-22:00',
                    'has_dryer': True
                },
                {
                    'name': 'ТЦ "Галерея"',
                    'address': 'пр. Победы, 23',
                    'latitude': 43.5892,
                    'longitude': 39.7245,
                    'price': 30.0,
                    'rating': 4.5,
                    'is_accessible': True,
                    'description': 'Современный торговый центр',
                    'working_hours': '10:00-22:00',
                    'has_dryer': True
                },
                {
                    'name': 'Ресторан "У моря"',
                    'address': 'Набережная, 45',
                    'latitude': 43.5823,
                    'longitude': 39.7189,
                    'price': 40.0,
                    'rating': 4.2,
                    'is_accessible': False,
                    'description': 'Ресторан с видом на море',
                    'working_hours': '09:00-23:00'
                }
            ]
            
            for toilet_data in test_toilets:
                toilet = Toilet(owner_id=business_user.id, **toilet_data)
                db.session.add(toilet)
            
            db.session.commit()
            print(f"\n✓ Добавлено {len(test_toilets)} тестовых туалетов")
    
    print("\n✅ Обновление базы данных завершено!")
