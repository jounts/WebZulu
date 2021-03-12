from django.db import models
from django.contrib.auth.models import User as UserAuth


class NameSpace(models.Model):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.name}'


class Layer(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=250)
    title = models.CharField(max_length=150)
    namespace = models.ForeignKey('NameSpace', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class User(models.Model):
    auth_user = models.OneToOneField(UserAuth, on_delete=models.SET_NULL, null=True, blank=True)

    def _str__(self):
        return f'{UserAuth.Username}'


class Project(models.Model):
    namespace = models.ForeignKey('NameSpace', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
