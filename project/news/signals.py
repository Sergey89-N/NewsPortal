from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post
from django.conf import settings

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get_or_create(name='common')[0]
        instance.groups.add(common_group)

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        for category in instance.categories.all():
            for subscriber in category.subscribers.all():
                subject = f'Новая статья в категории {category.name}'
                message = render_to_string('news/email/new_post_email.html', {
                    'post': instance,
                    'category': category,
                    'user': subscriber,
                })
                send_mail(
                    subject=subject,
                    message='',
                    from_email='noreply@newssportal.com',
                    recipient_list=[subscriber.email],
                    html_message=message,
                )

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать в NewsPortal!'
        message = render_to_string('news/email/welcome_email.html', {
            'user': instance,
        })
        send_mail(
            subject=subject,
            message='',
            from_email='noreply@newssportal.com',
            recipient_list=[instance.email],
            html_message=message,
        )

@receiver(post_save, sender=User)
def add_user_to_common_group_and_welcome(sender, instance, created, **kwargs):
    if created:
        try:
            common_group = Group.objects.get(name='common')
            instance.groups.add(common_group)
        except Group.DoesNotExist:
            print("Группа 'common' не найдена.")
        subject = "Добро пожаловать в NewsPortal!"
        message = (
            f"Привет, {instance.username}!\n\n"
            "Спасибо за регистрацию в NewsPortal. Мы рады видеть вас среди наших пользователей.\n\n"
            "С уважением, команда NewsPortal"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])
