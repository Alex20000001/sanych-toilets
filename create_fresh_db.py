import os
from app import app, db, User, Toilet

print("Создаем базу данных...")

with app.app_context():
    # Создаем все таблицы
    db.create_all()
    print("✓ Таблицы созданы")
    
    # Создаем бизнес-пользователя
    business_user = User(
        username='test_business',
        email='business@test.com',
        is_business=True
    )
    business_user.set_password('password123')
    db.session.add(business_user)
    
    # Создаем обычного пользователя
    regular_user = User(
        username='test_user',
        email='user@test.com',
        is_business=False
    )
    regular_user.set_password('password123')
    db.session.add(regular_user)
    
    db.session.commit()
    print("✓ Пользователи созданы:")
    print("  - business@test.com / password123 (бизнес)")
    print("  - user@test.com / password123 (обычный)")
    
    # Создаем тестовые туалеты
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
            'has_soap': True,
            'has_paper': True,
            'has_dryer': True,
            'has_mirror': True
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
            'has_soap': True,
            'has_paper': True,
            'has_dryer': True,
            'has_mirror': True
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
            'working_hours': '09:00-23:00',
            'has_soap': True,
            'has_paper': True,
            'has_dryer': False,
            'has_mirror': True
        }
    ]
    
    for toilet_data in test_toilets:
        toilet = Toilet(owner_id=business_user.id, **toilet_data)
        db.session.add(toilet)
    
    db.session.commit()
    print(f"✓ Создано {len(test_toilets)} тестовых туалетов")
    
    print("\n✅ База данных успешно создана!")
    
    # Проверяем результат
    print(f"\nПользователей в базе: {User.query.count()}")
    print(f"Туалетов в базе: {Toilet.query.count()}")
