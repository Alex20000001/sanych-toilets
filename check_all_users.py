from app import app, db, User

with app.app_context():
    print("=== Все пользователи в базе данных ===")
    users = User.query.all()
    for user in users:
        print(f"\nEmail: {user.email}")
        print(f"Username: {user.username}")
        print(f"Is Business: {user.is_business}")
        print(f"Password Hash exists: {bool(user.password_hash)}")
        print(f"Created at: {user.created_at}")
        
    print(f"\nВсего пользователей: {len(users)}")