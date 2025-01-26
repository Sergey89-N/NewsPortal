from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Category, Post
from datetime import datetime, timedelta

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
