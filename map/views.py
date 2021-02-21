from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        context = {'layer_list': ['Anivskiy_ST_SViV:vs', 'Anivskiy_ST_SViV:TS', 'Anivskiy_ST_SViV:vo']}

        return render(request, 'map/index.html', context)