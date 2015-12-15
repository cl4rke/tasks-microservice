from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class ApiKey(models.Model):
    value = models.CharField(max_length=255)
    user = models.OneToOneField(User)
    last_login = models.DateTimeField()

    def __str__(self):
        return "[%s] %s" % (self.user.username, self.value)


class Skill(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SkillValue(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    value = models.FloatField()

    def __str__(self):
        return "[%s] %s - %s" % (self.user.username, self.skill, self.value)

    def serialize(self):
        return {
                self.skill.name: self.value
                }


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(User, related_name='assigned_user_id', null=True, blank=True)
    estimated_time = models.IntegerField()
    time_completed = models.IntegerField(blank=True, null=True)
    is_completed = models.BooleanField()
    dependency = models.ForeignKey('Task', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_by_user_id')

    def __str__(self):
        return self.name

    def serialize(self):
        return {
                'name': self.name,
                'description': self.description,
                'assigned_to': self.assigned_to.username if self.assigned_to else None,
                'estimated_time': self.estimated_time,
                'time_completed': self.time_completed,
                'is_completed': self.is_completed,
                'dependency': self.dependency.serialize() if self.dependency else None,
                'created_by': self.created_by.username,
                }


class Absence(models.Model):
    date = models.DateField()
    is_approved = models.BooleanField()
    user = models.ForeignKey(User)

    def __str__(self):
        return "%s[%s] %s" % ('' if self.is_approved else '!!! ', self.user.username, self.date)

    def serialize(self):
        return {
                'username': self.user.username,
                'is_approved': self.is_approved,
                'date': self.date,
                }

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender_user_id')
    receiver = models.ForeignKey(User, related_name='receiver_user_id')
    content = models.TextField()

    def __str__(self):
        return "[%s --- %s] %s" % (self.sender, self.receiver, self.content)

    def serialize(self):
        return {
                'name': self.name,
                'sender': self.sender.username,
                'receiver': self.receiver.username,
                }

