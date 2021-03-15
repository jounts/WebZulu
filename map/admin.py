from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Project, NameSpace, Layer

from .tasks import import_zulu_data_task

admin.site.register(Layer)
admin.site.register(Project)


@admin.register(NameSpace)
class ImportZuluData(admin.ModelAdmin):
    change_list_template = 'variants/import_zulu_data.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-zulu-data/', self.import_zulu_data),
        ]
        return my_urls + urls

    def import_zulu_data(self, request):
        result = import_zulu_data_task.delay()
        self.message_user(
            request,
            f'Task ID: {result.task_id} was added to queue. Last known status: {result.status}'
        )
        return HttpResponseRedirect('../')
