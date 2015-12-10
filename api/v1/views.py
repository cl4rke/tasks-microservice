from django.http import JsonResponse, HttpResponseNotFound

def login(request):
    if request.method == 'POST':
        return JsonResponse({
            'data': {
                'api_key': '1234321',
                'username': 'user',
            },
        })

    else:
        return HttpResponseNotFound()

