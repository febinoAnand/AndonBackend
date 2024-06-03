
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            user_id = request.session.get(token)
            if user_id:
                try:
                    request.user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    request.user = None
            else:
                request.user = None
        else:
            request.user = None
