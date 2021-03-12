from django.shortcuts import render
from django.views import View

from WebZulu.settings import GIS_SERVER
from .common.zulu_auth import get_credentials
from .common.layers import get_centre_map


class MapAdminView(View):
    pass


class IndexView(View):
    def get(self, request):
        layers = ['Niznevartovsk_AST:Gaz', 'Niznevartovsk_AST:SanOchistka', 'Niznevartovsk_AST:Svet']# ['Anivskiy_ST_SViV:vs', 'Anivskiy_ST_SViV:vo', 'Anivskiy_ST_SViV:TS'] #['test:vs', 'test:ts']
        context = {'layer_list': layers}
        context.update({'credentials': get_credentials()})
        context.update({'GIS_SERVER': GIS_SERVER})
        context.update({'CENTRE_CORD': get_centre_map(layers)})

        return render(request, 'map/index.html', context)


class PublicView(View):
    def get(self, request):
        pass
