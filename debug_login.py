from app import app, db, User
from werkzeug.security import check_password_hash

with app.app_context():
    email = 'alex-1990-51@mail.ru'
    
    # Проверяем всех пользователей с похожим email
    print("=== Поиск пользователей ===")
    all_users = User.query.all()
    for u in all_users:
        if 'alex' in u.email.lower():
            print(f"Found: '{u.email}' (длина: {len(u.email)})")
    
    # Точный поиск
    user = User.query.filter_by(email=email).first()
    if user:
        print(f"\nПользователь найден: {user.email}")
        print(f"Username: {user.username}")
        print(f"Password hash: {user.password_hash[:20]}...")
        
        # Проверяем пароль напрямую
        test_password = input("Введите пароль для проверки: ")
        
        # Метод 1
        result1 = user.check_password(test_password)
        print(f"check_password: {result1}")
        
        # Метод 2
        result2 = check_password_hash(user.password_hash, test_password)
        print(f"check_password_hash: {result2}")
        
    else:
        print(f"Пользователь '{email}' НЕ НАЙДЕН!")
        print("\nВсе пользователи в базе:")
        for u in User.query.all():
            print(f"- '{u.email}'")