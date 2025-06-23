from django import template
from django.urls import reverse, NoReverseMatch
from django.core.cache import cache
from ..models import Menu, MenuItem

register = template.Library()


def normalize_url(url):
    if url.endswith('/') and url != '/':
        return url[:-1]
    return url

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Template tag для отрисовки древовидного меню
    
    Использование: {% draw_menu 'main_menu' %}
    
    Args:
        context: контекст шаблона
        menu_name: название меню для отрисовки
    """
    request = context.get('request')
    current_url = request.path if request else '/'
    
    # Ключ для кеширования
    cache_key = f'menu_{menu_name}_{current_url}'
    
    # Пытаемся получить меню из кеша
    menu_data = cache.get(cache_key)
    
    if menu_data is None:
        try:
            # Получаем меню из БД одним запросом с prefetch_related
            menu = Menu.objects.prefetch_related(
                'items__children__children__children'  # Поддерживаем до 4 уровней вложенности
            ).get(name=menu_name)
            
            # Получаем все пункты меню
            all_items = list(menu.items.filter(is_active=True).order_by('order'))
            
            # Определяем активный пункт и разворачиваем нужные ветки
            active_item = find_active_item(all_items, current_url)
            expanded_items = get_expanded_items(active_item, all_items)
            
            menu_data = {
                'menu': menu,
                'menu_tree': all_items,  # Передаем все активные пункты
                'active_item': active_item,
                'expanded_items': expanded_items,
                'menu_name': menu_name,
            }
            
            # Кешируем результат на 1 час
            cache.set(cache_key, menu_data, 3600)
            
        except Menu.DoesNotExist:
            menu_data = {
                'menu': None,
                'menu_tree': [],
                'active_item': None,
                'expanded_items': set(),
                'menu_name': menu_name,
            }
    
    return menu_data


def find_active_item(items, current_url):
    current_url = normalize_url(current_url)
    for item in items:
        try:
            item_url = normalize_url(item.get_url())
            if item_url == current_url:
                return item
        except NoReverseMatch:
            continue
    return None


def get_expanded_items(active_item, all_items):
    """
    Определяет какие пункты меню должны быть развернуты
    
    Правила:
    1. Все предки активного пункта развернуты
    2. Первый уровень вложенности под активным пунктом развернут
    
    Args:
        active_item: активный пункт меню
        all_items: список всех пунктов меню
        
    Returns:
        set: множество ID развернутых пунктов
    """
    expanded = set()
    
    if active_item:
        # Добавляем активный пункт
        expanded.add(active_item.id)
        
        # Добавляем всех предков
        ancestors = active_item.get_ancestors()
        for ancestor in ancestors:
            expanded.add(ancestor.id)
        
        # Добавляем детей активного пункта (первый уровень вложенности)
        children = active_item.get_children()
        for child in children:
            expanded.add(child.id)
    
    return expanded 