import os
from app import app, db

print("Проверяем настройки базы данных...")
print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Путь к app.py: {os.path.abspath('app.py')}")

# Ищем все .db файлы в текущей директории
print("\nФайлы .db в текущей директории:")
for file in os.listdir('.'):
    if file.endswith('.db'):
        print(f"  - {file} (размер: {os.path.getsize(file)} байт)")

# Проверяем instance папку (Flask иногда создает БД там)
instance_path = os.path.join(os.getcwd(), 'instance')
if os.path.exists(instance_path):
    print(f"\nФайлы в папке instance:")
    for file in os.listdir(instance_path):
        if file.endswith('.db'):
            print(f"  - {file} (размер: {os.path.getsize(os.path.join(instance_path, file))} байт)")
