from app import app, db, User, Toilet
import os

# Удаляем старую базу, если она существует
db_path = 'ssanych.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Старая база данных {db_path} удалена")

with app.app_context():
    # Создаём все таблицы
    db.create_all()
    print("Таблицы созданы успешно")
    
    # Создаем тестового бизнес-пользователя
    business_user = User(
        username='test_business',
        email='business@test.com',
        is_business=True
    )
    business_user.set_password('password123')
    db.session.add(business_user)
    db.session.commit()
    print("Бизнес-пользователь создан: business@test.com / password123")
    
    # Создаем обычного пользователя для тестирования
    regular_user = User(
        username='test_user',
        email='user@test.com',
        is_business=False
    )
    regular_user.set_password('password123')
    db.session.add(regular_user)
    db.session.commit()
    print("Обычный пользователь создан: user@test.com / password123")
    
    # Добавляем тестовые туалеты
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
    print(f"Добавлено {len(test_toilets)} тестовых туалетов")
    
    print("\nБаза данных создана успешно!")
    print("Теперь можете запустить приложение: python app.py")