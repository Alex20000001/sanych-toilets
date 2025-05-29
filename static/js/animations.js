// static/js/animations.js

// Инициализация анимаций при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов при скролле
    initScrollReveal();
    
    // Параллакс эффект
    initParallax();
    
    // Анимация счетчиков
    initCounters();
    
    // Анимация текста
    initTextAnimations();
    
    // Hover эффекты для карточек
    initCardAnimations();
    
    // Анимация навигации
    initNavAnimations();
    
    // Плавная прокрутка
    initSmoothScroll();
    
    // Анимация загрузки
    initLoadingAnimations();
});

// Анимация появления при скролле
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('revealed');
                    
                    // Добавляем специальные эффекты для разных элементов
                    if (entry.target.classList.contains('card')) {
                        entry.target.style.transform = 'translateY(0) scale(1)';
                    }
                }, index * 100); // Задержка для последовательной анимации
            }
        });
    }, observerOptions);
    
    // Наблюдаем за всеми элементами с классом scroll-reveal
    document.querySelectorAll('.scroll-reveal').forEach(el => {
        observer.observe(el);
    });
    
    // Специальная анимация для карточек туалетов
    document.querySelectorAll('.toilet-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
}

// Параллакс эффект
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax-element');
    
    if (parallaxElements.length === 0) return;
    
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(el => {
            const speed = el.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

// Анимация счетчиков
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 секунды
        const step = target / (duration / 16); // 60 FPS
        let current = 0;
        
        const updateCounter = () => {
            current += step;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
                // Добавляем эффект пульсации после завершения
                counter.classList.add('animate-pulse');
                setTimeout(() => {
                    counter.classList.remove('animate-pulse');
                }, 2000);
            }
        };
        
        // Запускаем анимацию когда элемент появляется на экране
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                updateCounter();
                observer.disconnect();
            }
        });
        
        observer.observe(counter);
    });
}

// Анимация текста
function initTextAnimations() {
    // Анимация печатания текста
    const typewriterElements = document.querySelectorAll('.typewriter');
    
    typewriterElements.forEach(el => {
        const text = el.textContent;
        el.textContent = '';
        let index = 0;
        
        function type() {
            if (index < text.length) {
                el.textContent += text.charAt(index);
                index++;
                setTimeout(type, 100);
            }
        }
        
        // Запускаем когда элемент виден
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                type();
                observer.disconnect();
            }
        });
        
        observer.observe(el);
    });
    
    // Анимация разделения текста
    document.querySelectorAll('.text-split').forEach(el => {
        const text = el.textContent;
        el.innerHTML = text.split('').map((char, i) => 
            `<span style="animation-delay: ${i * 0.05}s" class="char">${char}</span>`
        ).join('');
    });
}

// Анимация карточек
function initCardAnimations() {
    const cards = document.querySelectorAll('.card-animated');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Создаем эффект ripple
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            card.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
        
        // 3D эффект при движении мыши
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
        });
    });
}

// Анимация навигации
function initNavAnimations() {
    const navbar = document.querySelector('.navbar-custom');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Скрываем/показываем навигацию при скролле
        if (currentScroll > lastScroll && currentScroll > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        // Меняем стиль навигации при скролле
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
            navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        } else {
            navbar.classList.remove('scrolled');
            navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
        }
        
        lastScroll = currentScroll;
    });
    
    // Анимация мобильного меню
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu-animated');
    
    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            mobileToggle.classList.toggle('active');
            
            // Анимация иконки бургера
            const icon = mobileToggle.querySelector('i');
            if (mobileMenu.classList.contains('active')) {
                icon.style.transform = 'rotate(90deg)';
                icon.className = 'bi bi-x-lg';
            } else {
                icon.style.transform = 'rotate(0deg)';
                icon.className = 'bi bi-list';
            }
        });
    }
}

// Плавная прокрутка
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const offsetTop = target.getBoundingClientRect().top + window.pageYOffset;
                
                window.scrollTo({
                    top: offsetTop - 100,
                    behavior: 'smooth'
                });
                
                // Добавляем эффект подсветки целевого элемента
                target.classList.add('highlight');
                setTimeout(() => {
                    target.classList.remove('highlight');
                }, 2000);
            }
        });
    });
}

// Анимация загрузки
function initLoadingAnimations() {
    // Анимация кнопок при клике
    document.querySelectorAll('.btn-animated').forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Добавляем индикатор загрузки
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loader"></span> Загрузка...';
            this.disabled = true;
            
            // Симуляция загрузки (замените на реальный запрос)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
                
                // Эффект успеха
                this.classList.add('success');
                setTimeout(() => {
                    this.classList.remove('success');
                }, 1000);
            }, 2000);
        });
    });
    
    // Skeleton loading для карточек
    function showSkeleton() {
        const container = document.getElementById('toiletsList');
        if (!container) return;
        
        container.innerHTML = Array(3).fill('').map(() => `
            <div class="toilet-card skeleton">
                <div class="skeleton-line" style="width: 60%; height: 20px; margin-bottom: 10px;"></div>
                <div class="skeleton-line" style="width: 80%; height: 16px; margin-bottom: 10px;"></div>
                <div class="skeleton-line" style="width: 40%; height: 16px;"></div>
            </div>
        `).join('');
    }
    
    // Экспортируем функцию для использования
    window.showSkeleton = showSkeleton;
}

// Дополнительные эффекты
// Эффект печатной машинки для заголовков
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Анимация маркеров на карте
function animateMapMarkers(markers) {
    markers.forEach((marker, index) => {
        setTimeout(() => {
            marker.setOpacity(0);
            marker.addTo(map);
            
            // Плавное появление
            let opacity = 0;
            const fadeIn = setInterval(() => {
                opacity += 0.1;
                marker.setOpacity(opacity);
                
                if (opacity >= 1) {
                    clearInterval(fadeIn);
                    // Добавляем эффект bounce
                    const icon = marker._icon;
                    if (icon) {
                        icon.style.animation = 'bounce 0.5s ease';
                    }
                }
            }, 50);
        }, index * 100);
    });
}

// Экспортируем функции для использования
window.animateMapMarkers = animateMapMarkers;
window.typeWriter = typeWriter;

// Эффект частиц для фона
function createParticles() {
    const particlesContainer = document.querySelector('.particles-bg');
    if (!particlesContainer) return;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (Math.random() * 20 + 10) + 's';
        particlesContainer.appendChild(particle);
    }
}

// Запускаем создание частиц
createParticles();

// Прелоадер
window.addEventListener('load', () => {
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        preloader.style.opacity = '0';
        setTimeout(() => {
            preloader.style.display = 'none';
            
            // Запускаем анимации после загрузки
            document.querySelectorAll('.animate-on-load').forEach((el, index) => {
                setTimeout(() => {
                    el.classList.add('animated');
                }, index * 100);
            });
        }, 500);
    }
});