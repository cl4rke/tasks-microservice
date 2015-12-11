from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth import authenticate

def login(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])

        if user is not None:
            return JsonResponse({
                'data': {
                    'api_key': user.apikey.value,
                    'username': user.username,
                },
            })

        return JsonResponse({
            'data': {
                'message': 'Invalid credentials.',
            },
        }, status=422)

    return HttpResponseNotFound()

