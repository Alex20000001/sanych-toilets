from app import app, User

with app.app_context():
    user = User.query.filter_by(email='business@test.com').first()
    if user and user.check_password('password123'):
        print("Пароль правильный!")
    else:
        print("Пароль неправильный!")