from django.apps import AppConfig


class TreeMenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tree_menu'
    verbose_name = 'Древовидное меню'

    def ready(self):
        # Импортируем сигналы, чтобы Django о них узнал
        # и мог вызывать наши функции-обработчики.
        import tree_menu.signals 