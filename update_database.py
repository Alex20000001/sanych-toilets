from app import app, db, Toilet
from sqlalchemy import text

with app.app_context():
    # Добавляем новые колонки в таблицу
    try:
        with db.engine.connect() as conn:
            # Добавляем новые колонки
            columns_to_add = [
                ("description", "TEXT"),
                ("photo", "VARCHAR(500)"),
                ("working_hours", "VARCHAR(100) DEFAULT '24/7'"),
                ("has_soap", "BOOLEAN DEFAULT 1"),
                ("has_paper", "BOOLEAN DEFAULT 1"),
                ("has_dryer", "BOOLEAN DEFAULT 0"),
                ("has_mirror", "BOOLEAN DEFAULT 1")
            ]
            
            for column_name, column_type in columns_to_add:
                try:
                    conn.execute(text(f"ALTER TABLE toilet ADD COLUMN {column_name} {column_type}"))
                    print(f"Добавлена колонка: {column_name}")
                    conn.commit()
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"Колонка {column_name} уже существует")
                    else:
                        print(f"Ошибка при добавлении {column_name}: {e}")
    
    except Exception as e:
        print(f"Общая ошибка: {e}")
    
    # Обновляем существующие туалеты с примерными данными
    toilets = Toilet.query.all()
    for toilet in toilets:
        if not toilet.description:
            if "Кофейня" in toilet.name:
                toilet.description = "Уютная кофейня с чистым и комфортным туалетом. Всегда есть мыло и бумажные полотенца."
                toilet.photo = "/static/img/coffee-toilet.jpg"
                toilet.working_hours = "08:00-22:00"
                toilet.has_dryer = True
            elif "ТЦ" in toilet.name:
                toilet.description = "Современный торговый центр с несколькими туалетными комнатами на каждом этаже."
                toilet.photo = "/static/img/mall-toilet.jpg"
                toilet.working_hours = "10:00-22:00"
                toilet.has_dryer = True
            else:
                toilet.description = "Чистый и ухоженный туалет с базовыми удобствами."
                toilet.photo = "/static/img/default-toilet.jpg"
                toilet.working_hours = "09:00-21:00"
    
    db.session.commit()
    print("База данных успешно обновлена!")