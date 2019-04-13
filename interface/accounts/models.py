from django.db import models
from django.contrib.auth.models import User


class Host(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255)


class Origin(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255)


class Account(models.Model):
    """A Standard user account to own a websocket service."""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True,
            help_text='The unique identifier for a service connection')
    hosts = models.ManyToManyField(Host)
    origins = models.ManyToManyField(Origin)


