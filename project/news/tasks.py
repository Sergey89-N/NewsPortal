from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Category, Post
from datetime import datetime, timedelta
from django.conf import settings

@shared_task
def send_weekly_newsletter():
    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        if subscribers:
            last_week = datetime.now() - timedelta(days=7)
            new_posts = Post.objects.filter(categories=category, created_at__gte=last_week)
            if new_posts:
                for subscriber in subscribers:
                    subject = f'Новые статьи в категории {category.name} за неделю'
                    message = render_to_string('news/email/weekly_newsletter.html', {
                        'category': category,
                        'new_posts': new_posts,
                        'user': subscriber,
                    })
                    send_mail(
                        subject=subject,
                        message='',
                        from_email='noreply@newssportal.com',
                        recipient_list=[subscriber.email],
                        html_message=message,
                    )

@shared_task
def send_new_post_notification(post_id):
    """
    Отправляет уведомление подписчикам для каждой категории, к которой относится новая статья.
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return

    for category in post.categories.all():
        subscribers = category.subscribers.all()
        for user in subscribers:
            subject = f"Новая статья в категории {category.name}"
            article_url = settings.SITE_URL + reverse('news_detail', args=[post.pk])
            message = (
                f"Привет, {user.username}!\n\n"
                f"В категории '{category.name}' появилась новая статья:\n"
                f"Заголовок: {post.title}\n\n"
                f"Краткое содержание:\n{post.preview()}\n\n"
                f"Читать статью: {article_url}\n\n"
                "С уважением, NewsPortal"
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

@shared_task
def send_weekly_digest():
    """
    Отправляет еженедельный дайджест новых статей подписчикам для каждой категории.
    """
    week_ago = timezone.now() - timedelta(days=7)
    for category in Category.objects.all():
        posts = category.post_set.filter(created_at__gte=week_ago)
        if posts.exists():
            for subscriber in category.subscribers.all():
                subject = f"Еженедельная рассылка: новые статьи в категории {category.name}"
                message = (
                    f"Привет, {subscriber.username}!\n\n"
                    f"За последнюю неделю в категории '{category.name}' появились следующие статьи:\n\n"
                )
                for post in posts:
                    article_url = settings.SITE_URL + reverse('news_detail', args=[post.pk])
                    message += f"- {post.title}: {article_url}\n"
                message += "\nС уважением, NewsPortal"
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
