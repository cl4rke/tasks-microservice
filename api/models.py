from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class ApiKey(models.Model):
    value = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def __str__(self):
        return "[%s] %s" % (self.user.username, self.value)


class Skill(models.Model):
    name = models.CharField(max_length=255)


class SkillValue(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    value = models.IntegerField()


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(User, related_name='assigned_user_id')
    estimated_time = models.IntegerField()
    time_completed = models.IntegerField(blank=True, null=True)
    is_completed = models.BooleanField()
    dependency = models.ForeignKey('Task', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_by_user_id')


class Absence(models.Model):
    date = models.DateField()
    is_approved = models.BooleanField()
    user = models.ForeignKey(User)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender_user_id')
    receiver = models.ForeignKey(User, related_name='receiver_user_id')
    name = models.TextField()

