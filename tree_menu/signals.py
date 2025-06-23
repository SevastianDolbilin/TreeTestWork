from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import MenuItem, Menu

# Этот декоратор "подписывает" нашу функцию на события
# сохранения (post_save) и удаления (post_delete) для модели MenuItem.
@receiver([post_save, post_delete], sender=MenuItem)
def clear_cache_on_menu_item_change(sender, instance, **kwargs):
    """
    Сбрасывает весь кеш при изменении/удалении/добавлении любого пункта меню.

    Это самый простой и надежный способ для нашего случая. Он гарантирует,
    что любые изменения в админке будут немедленно отражены на сайте.
    """
    cache.clear()

# Также добавим сброс кэша при изменении самого Меню (например, описания).
@receiver([post_save, post_delete], sender=Menu)
def clear_cache_on_menu_change(sender, instance, **kwargs):
    """
    Сбрасывает весь кеш при изменении/удалении/добавлении меню.
    """
    cache.clear() 