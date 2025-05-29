# init_db.py
from app import app, db, User, Toilet
from datetime import datetime

def init_database(force_add_toilets=False):
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        print("Database tables created!")
        
        # Проверяем, есть ли уже данные
        if User.query.first() is None:
            print("Adding test data...")
            
            # Создаем тестового бизнес-пользователя
            business_user = User(
                username='demo_business',
                email='business@demo.com',
                is_business=True
            )
            business_user.set_password('demo123')
            db.session.add(business_user)
            
            # Создаем обычного пользователя
            regular_user = User(
                username='demo_user',
                email='user@demo.com',
                is_business=False
            )
            regular_user.set_password('demo123')
            db.session.add(regular_user)
            
            db.session.commit()
            print(f"Created demo users:")
            print(f"  Business user: business@demo.com / demo123")
            print(f"  Regular user: user@demo.com / demo123")
            
            # Добавляем тестовые туалеты
            test_toilets = [
                {
                    'name': 'Туалет у пляжа "Ривьера"',
                    'address': 'ул. Егорова, 1, Сочи',
                    'latitude': 43.5935,
                    'longitude': 39.7157,
                    'price': 50,
                    'rating': 4.5,
                    'is_accessible': True,
                    'description': 'Чистый туалет рядом с центральным пляжем',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'WC в парке "Дендрарий"',
                    'address': 'Курортный проспект, 74, Сочи',
                    'latitude': 43.5709,
                    'longitude': 39.7425,
                    'price': 40,
                    'rating': 4.2,
                    'is_accessible': True,
                    'description': 'Туалет в парке с красивым видом',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': False,
                    'has_mirror': True
                },
                {
                    'name': 'Туалет на Морвокзале',
                    'address': 'ул. Войкова, 1, Сочи',
                    'latitude': 43.5814,
                    'longitude': 39.7191,
                    'price': 60,
                    'rating': 4.0,
                    'is_accessible': True,
                    'description': 'Современный туалет в здании морского вокзала',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'WC "У Олимпийского"',
                    'address': 'Олимпийский проспект, 21, Сочи',
                    'latitude': 43.4048,
                    'longitude': 39.9554,
                    'price': 70,
                    'rating': 4.8,
                    'is_accessible': True,
                    'description': 'Премиум туалет в Олимпийском парке',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'Туалет на набережной',
                    'address': 'Приморская набережная, Сочи',
                    'latitude': 43.5763,
                    'longitude': 39.7246,
                    'price': 30,
                    'rating': 3.8,
                    'is_accessible': False,
                    'description': 'Простой туалет на набережной',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': False,
                    'has_mirror': False
                },
                {
                    'name': 'WC в ТЦ "Моремолл"',
                    'address': 'ул. Новая Заря, 7, Сочи',
                    'latitude': 43.3977,
                    'longitude': 39.9738,
                    'price': 45,
                    'rating': 4.6,
                    'is_accessible': True,
                    'description': 'Чистые туалеты в торговом центре',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'Городской туалет у ж/д вокзала',
                    'address': 'ул. Горького, 56, Сочи',
                    'latitude': 43.5937,
                    'longitude': 39.7258,
                    'price': 35,
                    'rating': 3.5,
                    'is_accessible': True,
                    'description': 'Круглосуточный туалет у вокзала',
                    'has_soap': True,
                    'has_paper': False,
                    'has_dryer': False,
                    'has_mirror': True,
                    'working_hours': '24/7'
                },
                {
                    'name': 'Туалет в парке "Ривьера"',
                    'address': 'ул. Егорова, 1, Сочи',
                    'latitude': 43.5906,
                    'longitude': 39.7168,
                    'price': 40,
                    'rating': 4.1,
                    'is_accessible': False,
                    'description': 'Туалет в популярном парке развлечений',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': False,
                    'has_mirror': True
                }
            ]
            
            for toilet_data in test_toilets:
                toilet = Toilet(
                    owner_id=business_user.id,
                    **toilet_data
                )
                db.session.add(toilet)
            
            db.session.commit()
            print(f"Added {len(test_toilets)} test toilets")
            print("Database initialization complete!")
        else:
            print("Database already contains data, skipping initialization")
        
        # Проверяем количество туалетов
        toilet_count = Toilet.query.count()
        if force_add_toilets or toilet_count < 8:
            print(f"Current toilet count: {toilet_count}")
            
            # Получаем бизнес-пользователя
            business_user = User.query.filter_by(is_business=True).first()
            if not business_user:
                print("No business user found, please run full initialization")
                return
            
            # Полный список всех туалетов
            all_toilets = [
                {
                    'name': 'Туалет у пляжа "Ривьера"',
                    'address': 'ул. Егорова, 1, Сочи',
                    'latitude': 43.5935,
                    'longitude': 39.7157,
                    'price': 50,
                    'rating': 4.5,
                    'is_accessible': True,
                    'description': 'Чистый туалет рядом с центральным пляжем',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'WC в парке "Дендрарий"',
                    'address': 'Курортный проспект, 74, Сочи',
                    'latitude': 43.5709,
                    'longitude': 39.7425,
                    'price': 40,
                    'rating': 4.2,
                    'is_accessible': True,
                    'description': 'Туалет в парке с красивым видом',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': False,
                    'has_mirror': True
                },
                {
                    'name': 'Туалет на Морвокзале',
                    'address': 'ул. Войкова, 1, Сочи',
                    'latitude': 43.5814,
                    'longitude': 39.7191,
                    'price': 60,
                    'rating': 4.0,
                    'is_accessible': True,
                    'description': 'Современный туалет в здании морского вокзала',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'WC "У Олимпийского"',
                    'address': 'Олимпийский проспект, 21, Сочи',
                    'latitude': 43.4048,
                    'longitude': 39.9554,
                    'price': 70,
                    'rating': 4.8,
                    'is_accessible': True,
                    'description': 'Премиум туалет в Олимпийском парке',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'Туалет на набережной',
                    'address': 'Приморская набережная, Сочи',
                    'latitude': 43.5763,
                    'longitude': 39.7246,
                    'price': 30,
                    'rating': 3.8,
                    'is_accessible': False,
                    'description': 'Простой туалет на набережной',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': False,
                    'has_mirror': False
                },
                {
                    'name': 'WC в ТЦ "Моремолл"',
                    'address': 'ул. Новая Заря, 7, Сочи',
                    'latitude': 43.3977,
                    'longitude': 39.9738,
                    'price': 45,
                    'rating': 4.6,
                    'is_accessible': True,
                    'description': 'Чистые туалеты в торговом центре',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': True,
                    'has_mirror': True
                },
                {
                    'name': 'Городской туалет у ж/д вокзала',
                    'address': 'ул. Горького, 56, Сочи',
                    'latitude': 43.5937,
                    'longitude': 39.7258,
                    'price': 35,
                    'rating': 3.5,
                    'is_accessible': True,
                    'description': 'Круглосуточный туалет у вокзала',
                    'has_soap': True,
                    'has_paper': False,
                    'has_dryer': False,
                    'has_mirror': True,
                    'working_hours': '24/7'
                },
                {
                    'name': 'Туалет в парке "Ривьера"',
                    'address': 'ул. Егорова, 1, Сочи',
                    'latitude': 43.5906,
                    'longitude': 39.7168,
                    'price': 40,
                    'rating': 4.1,
                    'is_accessible': False,
                    'description': 'Туалет в популярном парке развлечений',
                    'has_soap': True,
                    'has_paper': True,
                    'has_dryer': False,
                    'has_mirror': True
                }
            ]
            
            # Проверяем какие туалеты уже есть
            existing_toilets = Toilet.query.all()
            existing_names = [t.name for t in existing_toilets]
            
            # Добавляем только те, которых нет
            added_count = 0
            for toilet_data in all_toilets:
                if toilet_data['name'] not in existing_names:
                    toilet = Toilet(
                        owner_id=business_user.id,
                        **toilet_data
                    )
                    db.session.add(toilet)
                    added_count += 1
                    print(f"Added: {toilet_data['name']}")
            
            if added_count > 0:
                db.session.commit()
                print(f"Added {added_count} new toilets")
            else:
                print("All toilets already exist")

if __name__ == '__main__':
    import sys
    force = '--force' in sys.argv
    init_database(force_add_toilets=force)