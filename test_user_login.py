from app import app, db, User

with app.app_context():
    email = input("Введите email пользователя: ")
    password = input("Введите пароль: ")
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        print(f"Пользователь с email {email} НЕ НАЙДЕН!")
    else:
        print(f"\nПользователь найден:")
        print(f"Username: {user.username}")
        print(f"Is Business: {user.is_business}")
        
        if user.check_password(password):
            print("✓ Пароль ПРАВИЛЬНЫЙ!")
        else:
            print("✗ Пароль НЕПРАВИЛЬНЫЙ!")
            
            # Попробуем сбросить пароль
            reset = input("\nСбросить пароль? (y/n): ")
            if reset.lower() == 'y':
                new_password = input("Введите новый пароль: ")
                user.set_password(new_password)
                db.session.commit()
                print("Пароль успешно изменен!")