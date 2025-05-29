from app import app, db, User

with app.app_context():
    # Проверяем существующего пользователя
    user = User.query.filter_by(email='business@test.com').first()
    if user:
        print(f"Пользователь найден: {user.username}")
        print(f"Бизнес аккаунт: {user.is_business}")
        print(f"ID: {user.id}")
    else:
        print("Пользователь не найден, создаём...")
        
        # Создаем нового
        business_user = User(
            username='test_business',
            email='business@test.com',
            is_business=True
        )
        business_user.set_password('password123')
        db.session.add(business_user)
        db.session.commit()
        print("Бизнес-пользователь создан!")
    
    # Показываем всех пользователей
    print("\nВсе пользователи:")
    all_users = User.query.all()
    for u in all_users:
        print(f"- {u.email} (Бизнес: {u.is_business})")