from django.contrib.auth.models import User
from django.http import JsonResponse


def api_confirmation(view_func):
    def wrapped_view(request, *args, **kwargs):
        data = request.META

        if 'HTTP_X_AUTHORIZATION' not in data:
            return JsonResponse({
                'data': {
                    'message': 'Please specify X-Authorization.',
                },
            }, status=403)

        user = User.objects.filter(id=data['HTTP_X_AUTHORIZATION'])

        if not user.exists():
            return JsonResponse({
                'data': {
                    'message': 'Incorrect API key.',
                },
            }, status=401)

        request.user = user.first()

        return view_func(request, *args, **kwargs)
    return wrapped_view

