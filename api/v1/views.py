from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth import authenticate
from django.db.models import Q
from tasks_microservice.decorators import api_confirmation, form_validation
from api.models import *
from api import forms
from datetime import datetime


@form_validation('POST', forms.LoginForm)
def login(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])

        if user is not None:
            user.apikey.last_login = last_login=datetime.now()
            user.apikey.save()

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
@form_validation('POST', forms.ChangePasswordForm)
def change_password(request):
    if request.method == 'POST':
        data = request.POST
        user = request.user
        authorized = user.check_password(data['old_password'])

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


@api_confirmation
@form_validation('POST', forms.CreateTaskForm)
def tasks(request):
    if request.method == 'GET':
        return JsonResponse({
            'data': [task.serialize() for task in Task.objects.all()]
        })

    if request.method == 'POST':
        data = request.POST
        user = request.user

        task = Task(name=data['name'], description=data['description'], created_by=user, is_completed=False, estimated_time=data['estimated_time'])
        task.save()

        return JsonResponse({
            'data': {
                'message': 'Successfully added task!',
            },
        })

    return HttpResponseNotFound()


@api_confirmation
@form_validation('POST', forms.CreateMessageForm)
def messages(request):
    if request.method == 'GET':
        return JsonResponse({
            'data': [message.serialize() for message in Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))]
        })

    if request.method == 'POST':
        data = request.POST
        user = request.user

        message = Message(content=data['content'], receiver=User.objects.filter(username=data['username']).first(), sender=user)
        message.save()

        return JsonResponse({
            'data': {
                'message': 'Successfully sent message!',
            },
        })

    return HttpResponseNotFound()


@api_confirmation
@form_validation('POST', forms.CreateAbsenceForm)
def absences(request):
    if request.method == 'GET':
        return JsonResponse({
            'data': [absence.serialize() for absence in Absence.objects.all()]
        })

    if request.method == 'POST':
        data = request.POST
        user = request.user

        absence = Absence(date=data['date'], is_approved=False, user=user)
        absence.save()

        return JsonResponse({
            'data': {
                'message': 'Successfully requested absence!',
            },
        })

    return HttpResponseNotFound()


@api_confirmation
@form_validation('POST', forms.CreateSkillForm)
def skills(request):
    if request.method == 'GET':
        user = request.user
        return JsonResponse({
            'data': [skill_value.serialize() for skill_value in user.skillvalue_set.all()]
        })

    if request.method == 'POST':
        data = request.POST
        user = request.user

        skill = Skill.objects.filter(name__iexact=data['name']).first()
        skill_value = user.skillvalue_set.filter(skill=skill)

        if not skill_value.exists():
            skill_value = SkillValue(user=user, skill=skill, value=data['value'])
        else:
            skill_value = skill_value.first()
            skill_value.value = data['value']

        skill_value.save()

        return JsonResponse({
            'data': {
                'message': 'Successfully updated skill!',
            },
        })

    return HttpResponseNotFound()

