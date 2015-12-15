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


def required_fields(method, *fields):
    def decorator(view_func):
        def wrapped_view(request, *args2, **kwargs):
            if request.method == method:
                data = request.POST
                missing_fields = []

                for field in fields:
                    if field not in data:
                        missing_fields.append(field)

                print missing_fields

                if len(missing_fields):
                    return JsonResponse({
                        'data': {
                            'missing_fields': missing_fields,
                        },
                    }, status=422)

            return view_func(request)
        return wrapped_view
    return decorator

