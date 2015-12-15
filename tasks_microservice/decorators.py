from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import ApiKey


def api_confirmation(view_func):
    def wrapped_view(request, *args, **kwargs):
        data = request.META

        if 'HTTP_X_AUTHORIZATION' not in data:
            return JsonResponse({
                'data': {
                    'message': 'Please specify X-Authorization.',
                },
            }, status=403)

        api_key = ApiKey.objects.filter(value=data['HTTP_X_AUTHORIZATION'])

        if not api_key.exists():
            return JsonResponse({
                'data': {
                    'message': 'Incorrect API key.',
                },
            }, status=401)

        request.user = api_key.first().user

        return view_func(request, *args, **kwargs)
    return wrapped_view


def form_validation(method, form_class):
    def decorator(view_func):
        def wrapped_view(request, *args2, **kwargs):
            if request.method == method:
                data = request.POST
                form = form_class(data)

                if form.errors:
                    return JsonResponse({
                        'data': {
                            'errors': form.errors,
                        },
                    }, status=422)

            return view_func(request)
        return wrapped_view
    return decorator

