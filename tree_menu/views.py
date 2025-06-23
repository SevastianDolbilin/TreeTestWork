from django.shortcuts import render
from django.http import HttpResponse
from .models import Menu, MenuItem


def home(request):
    """Главная страница с демонстрацией меню"""
    return render(request, 'tree_menu/home.html', {
        'title': 'Главная страница',
        'content': 'Добро пожаловать! Это главная страница с демонстрацией древовидного меню.'
    })


def about(request):
    """Страница о проекте"""
    return render(request, 'tree_menu/page.html', {
        'title': 'О проекте',
        'content': 'Это демонстрационный проект древовидного меню на Django.'
    })


def services(request):
    """Страница услуг"""
    return render(request, 'tree_menu/page.html', {
        'title': 'Услуги',
        'content': 'Мы предоставляем различные услуги в области веб-разработки.'
    })


def service_detail(request, service_id):
    """Детальная страница услуги"""
    services_data = {
        '1': 'Веб-разработка - создание современных веб-сайтов и приложений.',
        '2': 'Мобильная разработка - разработка приложений для iOS и Android.',
        '3': 'Консультации - профессиональные консультации по IT вопросам.',
    }
    
    content = services_data.get(service_id, 'Услуга не найдена.')
    
    return render(request, 'tree_menu/page.html', {
        'title': f'Услуга {service_id}',
        'content': content
    })


def products(request):
    """Страница "Продукты" """
    return render(request, 'tree_menu/page.html', {
        'title': 'Продукты',
        'content': 'Наши продукты и решения.'
    })


def product_detail(request, product_id):
    """Детальная страница продукта"""
    products_data = {
        '1': 'Продукт 1 - инновационное решение для бизнеса.',
        '2': 'Продукт 2 - программное обеспечение для автоматизации.',
        '3': 'Продукт 3 - облачная платформа для управления данными.',
    }
    
    content = products_data.get(product_id, 'Продукт не найден.')
    
    return render(request, 'tree_menu/page.html', {
        'title': f'Продукт {product_id}',
        'content': content
    })


def contact(request):
    """Страница контактов"""
    return render(request, 'tree_menu/page.html', {
        'title': 'Контакты',
        'content': 'Свяжитесь с нами по email: contact@example.com'
    })


def blog(request):
    """Страница "Блог" """
    return render(request, 'tree_menu/page.html', {
        'title': 'Блог',
        'content': 'Наши статьи и новости.'
    })


def blog_post(request, post_id):
    """Страница отдельной статьи блога"""
    posts_data = {
        '1': 'Статья 1 - Новые технологии в веб-разработке.',
        '2': 'Статья 2 - Тренды мобильной разработки в 2024 году.',
        '3': 'Статья 3 - Как выбрать правильную технологию для проекта.',
    }
    
    content = posts_data.get(post_id, 'Статья не найдена.')
    
    return render(request, 'tree_menu/page.html', {
        'title': f'Статья {post_id}',
        'content': content
    })


def load_menu(request, menu_name):
    """AJAX endpoint для загрузки меню"""
    try:
        from django.template.loader import render_to_string
        from django.template import Context
        
        # Создаем контекст для template tag
        context = {
            'request': request,
            'menu_name': menu_name,
        }
        
        # Рендерим меню через template tag
        from .templatetags.menu_tags import draw_menu
        menu_data = draw_menu(context, menu_name)
        
        # Рендерим HTML меню
        menu_html = render_to_string('tree_menu/menu.html', menu_data, request=request)
        
        return HttpResponse(menu_html)
    except Exception as e:
        return HttpResponse(f'<div style="text-align: center; padding: 20px; color: #f44336;">Ошибка загрузки меню: {str(e)}</div>')


def test(request):
    """Тестовая страница для проверки template tags"""
    return render(request, 'tree_menu/test.html') 