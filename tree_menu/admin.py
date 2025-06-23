from django.contrib import admin
from django.utils.html import format_html
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    """Inline для отображения дочерних пунктов меню"""
    model = MenuItem
    extra = 0
    fields = ['title', 'url', 'named_url', 'order', 'is_active']
    ordering = ['order']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Админка для модели Menu"""
    list_display = ['name', 'description', 'items_count']
    search_fields = ['name', 'description']
    inlines = [MenuItemInline]
    
    def items_count(self, obj):
        """Количество пунктов в меню"""
        return obj.items.count()
    items_count.short_description = 'Количество пунктов'


class MenuItemChildrenInline(admin.TabularInline):
    """Inline для отображения дочерних пунктов"""
    model = MenuItem
    extra = 0
    fields = ['title', 'url', 'named_url', 'order', 'is_active']
    ordering = ['order']
    verbose_name = 'Дочерний пункт'
    verbose_name_plural = 'Дочерние пункты'
    
    def get_queryset(self, request):
        """Получить только дочерние пункты"""
        qs = super().get_queryset(request)
        if hasattr(self, 'parent_instance'):
            return qs.filter(parent=self.parent_instance)
        return qs


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Админка для модели MenuItem"""
    list_display = [
        'title', 'menu', 'parent', 'url_display', 
        'order', 'is_active', 'children_count'
    ]
    list_filter = ['menu', 'parent', 'is_active']
    search_fields = ['title', 'url', 'named_url']
    ordering = ['menu', 'order', 'title']
    inlines = [MenuItemChildrenInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('menu', 'parent', 'title', 'is_active')
        }),
        ('URL', {
            'fields': ('url', 'named_url'),
            'description': 'Укажите либо URL, либо Named URL (но не оба)'
        }),
        ('Порядок', {
            'fields': ('order',)
        }),
    )
    
    def url_display(self, obj):
        """Отображение URL в админке"""
        if obj.url:
            return format_html('<span style="color: green;">{}</span>', obj.url)
        elif obj.named_url:
            return format_html('<span style="color: blue;">{}</span>', obj.named_url)
        return format_html('<span style="color: red;">Не указан</span>')
    url_display.short_description = 'URL'
    
    def children_count(self, obj):
        """Количество дочерних пунктов"""
        return obj.children.count()
    children_count.short_description = 'Дочерние пункты'
    
    def get_form(self, request, obj=None, **kwargs):
        """Настройка формы для фильтрации parent по menu"""
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.menu:
            # Фильтруем parent только пунктами из того же меню
            form.base_fields['parent'].queryset = MenuItem.objects.filter(
                menu=obj.menu
            ).exclude(id=obj.id)
        return form
    
    def save_model(self, request, obj, form, change):
        """Сохранение модели с установкой parent_instance для inline"""
        super().save_model(request, obj, form, change)
        self.parent_instance = obj 