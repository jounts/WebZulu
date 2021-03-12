from django.db import models
from django.contrib.auth.models import User as UserAuth


class NameSpace(models.Model):
    name = models.Charfield(max_length=150)
    short_name = models.Charfield(max_length=50, blank=True)

    def __str__(self):
        return f'{self.name}'

class Layer(models.Model):
    name = models.Charfield(max_length=100)
    full_name = models.Charfield(max_length=250)
    title = models.Charfield(max_length=150)

    def __str__(self):
        return f'{self.name}'


class User(models.Model):
    auth_user = models.OneToOneField(UserAuth, on_delete=models.CASCADE)
    
    def _str__(self):
        return f{UserAuth.name}
        