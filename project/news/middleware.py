import pytz
from django.utils import timezone

class TimezoneMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'author'):
            tzname = request.user.author.timezone
            try:
                timezone.activate(pytz.timezone(tzname))
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response
