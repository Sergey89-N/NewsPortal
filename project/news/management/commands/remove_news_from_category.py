from django.core.management.base import BaseCommand
from django.db.models import Q
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории после подтверждения.'

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help='Название категории')

    def handle(self, *args, **kwargs):
        category_name = kwargs['category_name']

        # Проверяем, существует ли категория
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория "{category_name}" не найдена.'))
            return

        # Получаем все новости в этой категории
        posts = Post.objects.filter(categories=category)

        if not posts.exists():
            self.stdout.write(self.style.WARNING(f'В категории "{category_name}" нет новостей.'))
            return

        # Выводим список новостей для удаления
        self.stdout.write(self.style.WARNING(f'Найдено {posts.count()} новостей в категории "{category_name}":'))
        for post in posts:
            self.stdout.write(f'- {post.title}')

        # Запрашиваем подтверждение
        confirm = input('Вы уверены, что хотите удалить эти новости? (yes/no): ').strip().lower()
        if confirm != 'yes':
            self.stdout.write(self.style.WARNING('Удаление отменено.'))
            return

        # Удаляем новости
        posts.delete()
        self.stdout.write(self.style.SUCCESS(f'Все новости из категории "{category_name}" успешно удалены.'))
