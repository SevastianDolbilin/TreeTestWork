from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError


class Menu(models.Model):
    """Модель для группировки пунктов меню"""
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Название меню'
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание'
    )
    
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель для пунктов меню с поддержкой иерархии"""
    menu = models.ForeignKey(
        Menu, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='Меню'
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Родительский пункт'
    )
    title = models.CharField(
        max_length=100, 
        verbose_name='Название'
    )
    url = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name='URL'
    )
    named_url = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='Named URL'
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name='Порядок'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активно'
    )
    
    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['menu', 'order', 'title']
        unique_together = ['menu', 'parent', 'order']
    
    def __str__(self):
        return f"{self.title} ({self.menu.name})"
    
    def clean(self):
        """Валидация: должен быть указан либо url, либо named_url"""
        if not self.url and not self.named_url:
            raise ValidationError(
                'Необходимо указать либо URL, либо Named URL'
            )
        if self.url and self.named_url:
            raise ValidationError(
                'Можно указать только один из вариантов: URL или Named URL'
            )
        # Новая проверка: Явный URL должен быть абсолютным путем.
        if self.url and not self.url.startswith('/') and not self.url.startswith('http'):
            raise ValidationError({
                'url': 'Ошибка: Явный URL должен начинаться со слэша "/" (например, "/services/") или с "http".'
            })
    
    def get_url(self):
        """Получить URL для пункта меню"""
        if self.url:
            return self.url
        elif self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return '#'
    
    def get_absolute_url(self):
        """Получить абсолютный URL для пункта меню"""
        return self.get_url()
    
    def get_children(self):
        """Получить дочерние пункты меню"""
        return self.children.filter(is_active=True).order_by('order')
    
    def get_ancestors(self):
        """Получить всех предков пункта меню"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return list(reversed(ancestors))
    
    def get_siblings(self):
        """Получить соседние пункты меню (с тем же родителем)"""
        if self.parent:
            return self.parent.get_children().exclude(id=self.id)
        else:
            return MenuItem.objects.filter(
                menu=self.menu, 
                parent=None, 
                is_active=True
            ).exclude(id=self.id).order_by('order') 