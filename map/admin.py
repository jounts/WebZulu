from django.contrib import admin

from .models import Project, NameSpace, Layer

admin.site.register(NameSpace)
admin.site.register(Layer)
admin.site.register(Project)