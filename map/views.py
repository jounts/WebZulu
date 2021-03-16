from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View, generic

from .models import Project, NameSpace, Layer

from .common.zulu_auth import get_credentials
from .common.layers import get_centre_map

from WebZulu.settings import GIS_SERVER


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        project = Project.objects.filter(user=request.user).first()

        if not isinstance(project, type(None)):
            namespace = project.namespace

            if project:
                layers = list(Layer.objects.filter(
                    namespace=NameSpace.objects.get(
                        name=namespace
                    )).values())
            else:
                layers = []
            context = {'namespace': namespace}
            context.update({'layer_list': layers})
            context.update({'gis_server': GIS_SERVER})
            context.update({'credentials': get_credentials()})
            context.update({'centre': get_centre_map(layers)})

            return render(request, 'map/index.html', context)
        return redirect('accounts/login')
