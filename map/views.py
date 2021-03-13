from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View, generic

from .models import Project, NameSpace, Layer

from .common.zulu_auth import get_credentials
from .common.layers import get_centre_map, parse_layers


class MapAdminView(View):
    def get(self, request):
        parse_layers()
        html = 'LayerList is updating'
        return HttpResponse(html)


class MapIndexView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'map/user_map.html'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        project = Project.objects.filter(user=request.user).first()
        namespace = project.namespace
        if project:
            layers = Layer.objects.filter(
                namespace=NameSpace.objects.get(
                    name=namespace
                )
            )
            print(list(layers.values()))
        else:
            layers = []
        context = {'layer_list': list(layers.values())}
        context.update({'credentials': get_credentials()})
        context.update({'CENTRE_CORD': get_centre_map(list(layers.values()))})

        return render(request, 'map/index.html', context)


class PublicView(View):
    def get(self, request):
        pass
