import pytz
from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag(takes_context=True)
def get_theme(context):

    user = context.get('user')
    if user and user.is_authenticated and hasattr(user, 'author') and user.author.timezone:
        try:
            tz = pytz.timezone(user.author.timezone)
            local_now = timezone.now().astimezone(tz)
        except Exception:
            local_now = timezone.localtime(timezone.now())
    else:
        local_now = timezone.localtime(timezone.now())

    hour = local_now.hour
    if hour < 6 or hour >= 18:
        return "dark"
    return "light"
