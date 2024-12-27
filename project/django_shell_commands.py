# Импорт моделей и функций
from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# Создание пользователей
user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

# Создание объектов модели Author
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавление категорий
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Технологии')

# Добавление статей и новости
post1 = Post.objects.create(author=author1, post_type=Post.ARTICLE, title='Статья 1', content='Содержание статьи 1')
post2 = Post.objects.create(author=author2, post_type=Post.ARTICLE, title='Статья 2', content='Содержание статьи 2')
post3 = Post.objects.create(author=author1, post_type=Post.NEWS, title='Новость 1', content='Содержание новости 1')

# Присвоение категорий
post1.categories.add(category1, category2)
post2.categories.add(category3)
post3.categories.add(category4)

# Создание комментариев
comment1 = Comment.objects.create(post=post1, user=user1, text='Комментарий 1 к статье 1')
comment2 = Comment.objects.create(post=post2, user=user2, text='Комментарий 1 к статье 2')
comment3 = Comment.objects.create(post=post3, user=user1, text='Комментарий 1 к новости 1')
comment4 = Comment.objects.create(post=post1, user=user2, text='Комментарий 2 к статье 1')

# Корректировка рейтингов
post1.like()
post1.like()
post2.dislike()
post3.like()
post3.like()
post3.like()

comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

# Обновление рейтингов пользователей
author1.update_rating()
author2.update_rating()

# Вывод лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, Рейтинг: {best_author.rating}")

# Вывод лучшей статьи
best_post = Post.objects.order_by('-rating').first()
print(f"Дата: {best_post.created_at}, Автор: {best_post.author.user.username}, Рейтинг: {best_post.rating}, Заголовок: {best_post.title}, Превью: {best_post.preview()}")

# Вывод всех комментариев к лучшей статье
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f"Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}")