# app.py
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
import qrcode
import io
import base64
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ЗАМЕНИТЬ ЭТИ 3 СТРОКИ КОНФИГА:
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ssanych.db')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модели базы данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_business = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    toilets = db.relationship('Toilet', backref='owner', lazy=True)
    visits = db.relationship('Visit', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Toilet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    is_accessible = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Новые поля
    description = db.Column(db.Text)
    photo = db.Column(db.String(500))
    working_hours = db.Column(db.String(100), default='24/7')
    has_soap = db.Column(db.Boolean, default=True)
    has_paper = db.Column(db.Boolean, default=True)
    has_dryer = db.Column(db.Boolean, default=False)
    has_mirror = db.Column(db.Boolean, default=True)
    
    # Отношения
    visits = db.relationship('Visit', backref='toilet', lazy=True)
    reviews = db.relationship('Review', backref='toilet', lazy=True)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    toilet_id = db.Column(db.Integer, db.ForeignKey('toilet.id'), nullable=False)
    qr_code = db.Column(db.String(100), unique=True, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    toilet_id = db.Column(db.Integer, db.ForeignKey('toilet.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Декоратор для бизнес-пользователей
def business_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_business:
            flash('Доступ только для бизнес-аккаунтов', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# API для получения списка туалетов
@app.route('/api/toilets')
def get_toilets():
    # Получаем параметры фильтрации
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    is_accessible = request.args.get('is_accessible', type=bool)
    
    # Базовый запрос
    query = Toilet.query.filter_by(is_active=True)
    
    # Применяем фильтры
    if min_price is not None:
        query = query.filter(Toilet.price >= min_price)
    if max_price is not None:
        query = query.filter(Toilet.price <= max_price)
    if min_rating is not None:
        query = query.filter(Toilet.rating >= min_rating)
    if is_accessible is not None:
        query = query.filter(Toilet.is_accessible == is_accessible)
    
    toilets = query.all()
    
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'address': t.address,
        'latitude': t.latitude,
        'longitude': t.longitude,
        'price': t.price,
        'rating': t.rating,
        'is_accessible': t.is_accessible,
        'description': t.description,
        'photo': t.photo,
        'working_hours': t.working_hours,
        'has_soap': t.has_soap,
        'has_paper': t.has_paper,
        'has_dryer': t.has_dryer,
        'has_mirror': t.has_mirror
    } for t in toilets])

# API для создания визита (оплаты)
@app.route('/api/visits', methods=['POST'])
@login_required
def create_visit():
    data = request.get_json()
    toilet_id = data.get('toilet_id')
    
    toilet = Toilet.query.get(toilet_id)
    if not toilet:
        return jsonify({'error': 'Toilet not found'}), 404
    
    # Генерируем уникальный QR-код
    qr_code = secrets.token_urlsafe(32)
    
    # Создаем визит
    visit = Visit(
        user_id=current_user.id,
        toilet_id=toilet_id,
        qr_code=qr_code,
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )
    
    db.session.add(visit)
    db.session.commit()
    
    # Генерируем QR-код изображение
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_code)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    img_base64 = base64.b64encode(img_io.getvalue()).decode()
    
    return jsonify({
        'visit_id': visit.id,
        'qr_code': qr_code,
        'qr_image': f'data:image/png;base64,{img_base64}',
        'expires_at': visit.expires_at.isoformat()
    })

# API для проверки QR-кода (для IoT-замков)
@app.route('/api/verify-qr', methods=['POST'])
def verify_qr():
    data = request.get_json()
    qr_code = data.get('qr_code')
    toilet_id = data.get('toilet_id')
    
    visit = Visit.query.filter_by(
        qr_code=qr_code,
        toilet_id=toilet_id,
        is_used=False
    ).first()
    
    if not visit:
        return jsonify({'valid': False, 'message': 'Invalid QR code'}), 400
    
    if visit.expires_at < datetime.utcnow():
        return jsonify({'valid': False, 'message': 'QR code expired'}), 400
    
    # Помечаем визит как использованный
    visit.is_used = True
    visit.used_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'valid': True, 'message': 'Access granted'})

# Бизнес-панель
@app.route('/business')
@login_required
@business_required
def business_dashboard():
    return render_template('business_dashboard.html')

# API для бизнес-аналитики
@app.route('/api/business/stats')
@login_required
@business_required
def business_stats():
    # Получаем статистику по туалетам владельца
    toilets = Toilet.query.filter_by(owner_id=current_user.id).all()
    
    stats = []
    for toilet in toilets:
        # Считаем визиты за последние 30 дней
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        visits_count = Visit.query.filter(
            Visit.toilet_id == toilet.id,
            Visit.created_at >= thirty_days_ago
        ).count()
        
        # Считаем доход
        revenue = visits_count * toilet.price
        
        stats.append({
            'toilet_id': toilet.id,
            'name': toilet.name,
            'visits_last_30_days': visits_count,
            'revenue_last_30_days': revenue,
            'rating': toilet.rating,
            'total_reviews': len(toilet.reviews)
        })
    
    return jsonify(stats)

# API для добавления туалета (для бизнеса)
@app.route('/api/business/toilets', methods=['POST'])
@login_required
@business_required
def add_toilet():
    data = request.get_json()
    
    toilet = Toilet(
        name=data['name'],
        address=data['address'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        price=data['price'],
        is_accessible=data.get('is_accessible', False),
        description=data.get('description', ''),
        working_hours=data.get('working_hours', '24/7'),
        has_soap=data.get('has_soap', True),
        has_paper=data.get('has_paper', True),
        has_dryer=data.get('has_dryer', False),
        has_mirror=data.get('has_mirror', True),
        owner_id=current_user.id
    )
    
    db.session.add(toilet)
    db.session.commit()
    
    return jsonify({
        'id': toilet.id,
        'message': 'Toilet added successfully'
    })

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Проверяем, существует ли пользователь
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'success': False, 'error': 'Email already registered'}), 400
            
            user = User(
                username=data['username'],
                email=data['email'],
                is_business=data.get('is_business', False)
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            print(f"New user registered: {user.email}")
            
            return jsonify({'success': True, 'message': 'Registration successful'})
        except Exception as e:
            print(f"Registration error: {e}")
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Registration failed'}), 500
    
    return render_template('register.html')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(f"=== LOGIN DEBUG ===")
            print(f"Raw data: {data}")
            
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            print(f"Email: '{email}' (length: {len(email)})")
            print(f"Password received: {'*' * len(password)}")
            
            user = User.query.filter_by(email=email).first()
            
            if not user:
                print(f"User not found: '{email}'")
                return jsonify({
                    'success': False,
                    'error': 'Пользователь не найден'
                }), 401
            
            print(f"User found: {user.email}")
            
            if not user.check_password(password):
                print(f"Invalid password for: '{email}'")
                return jsonify({
                    'success': False,
                    'error': 'Неверный пароль'
                }), 401
            
            login_user(user, remember=True)
            print(f"Login successful for: {user.email}, is_business: {user.is_business}")
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'is_business': user.is_business,
                'redirect': '/business' if user.is_business else '/'
            })
                
        except Exception as e:
            print(f"Login error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': 'Login failed'
            }), 500
    
    return render_template('login.html')

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Профиль пользователя
@app.route('/profile')
@login_required
def profile():
    # Получаем посещения пользователя
    visits = Visit.query.filter_by(user_id=current_user.id).order_by(Visit.created_at.desc()).limit(10).all()
    
    # Подсчитываем статистику
    visit_count = Visit.query.filter_by(user_id=current_user.id).count()
    
    # Считаем общую сумму потраченных денег
    total_spent = 0
    for visit in Visit.query.filter_by(user_id=current_user.id).all():
        toilet = Toilet.query.get(visit.toilet_id)
        if toilet:
            total_spent += toilet.price
    
    # Активные QR-коды
    active_qr_count = Visit.query.filter_by(
        user_id=current_user.id, 
        is_used=False
    ).filter(Visit.expires_at > datetime.utcnow()).count()
    
    # Для каждого визита добавляем информацию о туалете и цене
    for visit in visits:
        visit.toilet = Toilet.query.get(visit.toilet_id)
        visit.price = visit.toilet.price if visit.toilet else 0
        visit.is_active = not visit.is_used and visit.expires_at > datetime.utcnow()
        if visit.is_active:
            # Генерируем QR-код изображение для активных визитов
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(visit.qr_code)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            visit.qr_image = f'data:image/png;base64,{base64.b64encode(img_io.getvalue()).decode()}'
    
    return render_template('profile.html',
                         visits=visits,
                         page=1,
                         total_pages=1,
                         visit_count=visit_count,
                         total_spent=total_spent,
                         active_qr_count=active_qr_count)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)