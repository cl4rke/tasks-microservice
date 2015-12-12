from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth import authenticate
from tasks_microservice.decorators import api_confirmation


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


@api_confirmation
def change_password(request):
    if request.method == 'POST':
        data = request.POST
        authorized = request.user.check_password(data['old_password'])

        if not authorized:
            return JsonResponse({
                'data': {
                    'message': 'Incorrect old password.',
                }
            }, status=422)

        if data['password'] != data['password_confirmation']:
            return JsonResponse({
                'data': {
                    'message': 'Passwords do not match.',
                }
            }, status=422)

        user.set_password(data['password'])
        user.save()

        return JsonResponse({
            'data': {
                'message': 'Successfully changed password.',
            },
        })

    return HttpResponseNotFound()

