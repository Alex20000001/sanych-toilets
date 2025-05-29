from app import app, db, Toilet, User
import json

with app.app_context():
    print("=== ПРОВЕРКА БАЗЫ ДАННЫХ ===\n")
    
    # Проверяем пользователей
    users = User.query.all()
    print(f"Всего пользователей: {len(users)}")
    for user in users:
        print(f"  - {user.email} (ID: {user.id}, бизнес: {user.is_business})")
    
    # Проверяем туалеты
    print(f"\nВсего туалетов в базе: {Toilet.query.count()}")
    
    toilets = Toilet.query.all()
    for toilet in toilets:
        print(f"\nТуалет #{toilet.id}:")
        print(f"  Название: {toilet.name}")
        print(f"  Адрес: {toilet.address}")
        print(f"  Координаты: {toilet.latitude}, {toilet.longitude}")
        print(f"  Цена: {toilet.price}")
        print(f"  Рейтинг: {toilet.rating}")
        print(f"  Активен: {toilet.is_active}")
        print(f"  Доступен для инвалидов: {toilet.is_accessible}")
        print(f"  Владелец ID: {toilet.owner_id}")
    
    # Проверяем API endpoint
    print("\n=== ПРОВЕРКА API ===")
    
    with app.test_client() as client:
        # Тест API без фильтров
        response = client.get('/api/toilets')
        print(f"\nGET /api/toilets")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"Получено туалетов: {len(data)}")
            if data:
                print("\nПервый туалет из API:")
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка: {response.data.decode()}")
        
        # Тест с фильтрами
        response = client.get('/api/toilets?min_price=0&max_price=100')
        print(f"\nGET /api/toilets?min_price=0&max_price=100")
        print(f"Статус: {response.status_code}")
        print(f"Получено туалетов: {len(response.get_json()) if response.status_code == 200 else 'Ошибка'}")
    
    # Проверяем структуру таблицы
    print("\n=== СТРУКТУРА ТАБЛИЦЫ toilet ===")
    from sqlalchemy import inspect
    
    inspector = inspect(db.engine)
    columns = inspector.get_columns('toilet')
    
    for col in columns:
        print(f"  {col['name']}: {col['type']}")
