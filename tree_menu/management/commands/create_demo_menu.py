from django.core.management.base import BaseCommand
from tree_menu.models import Menu, MenuItem


class Command(BaseCommand):
    help = 'Создает демонстрационное меню для тестирования'

    def handle(self, *args, **options):
        self.stdout.write('Создание демонстрационного меню...')
        
        # Создаем главное меню
        menu, created = Menu.objects.get_or_create(
            name='main_menu',
            defaults={'description': 'Главное навигационное меню сайта'}
        )
        
        if created:
            self.stdout.write(f'Создано меню: {menu.name}')
        else:
            self.stdout.write(f'Меню {menu.name} уже существует')
        
        # Удаляем существующие пункты меню
        MenuItem.objects.filter(menu=menu).delete()
        
        # Создаем корневые пункты меню
        home = MenuItem.objects.create(
            menu=menu,
            title='Главная',
            named_url='tree_menu:home',
            order=1
        )
        
        about = MenuItem.objects.create(
            menu=menu,
            title='О нас',
            named_url='tree_menu:about',
            order=2
        )
        
        services = MenuItem.objects.create(
            menu=menu,
            title='Услуги',
            named_url='tree_menu:services',
            order=3
        )
        
        products = MenuItem.objects.create(
            menu=menu,
            title='Продукты',
            named_url='tree_menu:products',
            order=4
        )
        
        blog = MenuItem.objects.create(
            menu=menu,
            title='Блог',
            named_url='tree_menu:blog',
            order=5
        )
        
        contact = MenuItem.objects.create(
            menu=menu,
            title='Контакты',
            named_url='tree_menu:contact',
            order=6
        )
        
        # Создаем дочерние пункты для услуг
        service1 = MenuItem.objects.create(
            menu=menu,
            parent=services,
            title='Веб-разработка',
            named_url='tree_menu:service_detail',
            order=1
        )
        
        service2 = MenuItem.objects.create(
            menu=menu,
            parent=services,
            title='Мобильная разработка',
            named_url='tree_menu:service_detail',
            order=2
        )
        
        service3 = MenuItem.objects.create(
            menu=menu,
            parent=services,
            title='Консультации',
            named_url='tree_menu:service_detail',
            order=3
        )
        
        # Создаем дочерние пункты для продуктов
        product1 = MenuItem.objects.create(
            menu=menu,
            parent=products,
            title='Продукт 1',
            named_url='tree_menu:product_detail',
            order=1
        )
        
        product2 = MenuItem.objects.create(
            menu=menu,
            parent=products,
            title='Продукт 2',
            named_url='tree_menu:product_detail',
            order=2
        )
        
        product3 = MenuItem.objects.create(
            menu=menu,
            parent=products,
            title='Продукт 3',
            named_url='tree_menu:product_detail',
            order=3
        )
        
        # Создаем дочерние пункты для блога
        post1 = MenuItem.objects.create(
            menu=menu,
            parent=blog,
            title='Статья 1',
            named_url='tree_menu:blog_post',
            order=1
        )
        
        post2 = MenuItem.objects.create(
            menu=menu,
            parent=blog,
            title='Статья 2',
            named_url='tree_menu:blog_post',
            order=2
        )
        
        post3 = MenuItem.objects.create(
            menu=menu,
            parent=blog,
            title='Статья 3',
            named_url='tree_menu:blog_post',
            order=3
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Демонстрационное меню создано успешно! '
                f'Создано {MenuItem.objects.filter(menu=menu).count()} пунктов меню.'
            )
        ) 