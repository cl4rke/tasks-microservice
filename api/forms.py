from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    password = forms.CharField()
    password_confirmation = forms.CharField()


class CreateTaskForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    estimated_time = forms.FloatField()


class CreateMessageForm(forms.Form):
    content = forms.CharField()
    username = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']
        user = User.objects.filter(username=data)

        if not user.exists():
            raise forms.ValidationError("Username is invalid!")

        return data


class CreateAbsenceForm(forms.Form):
    date = forms.DateField()

