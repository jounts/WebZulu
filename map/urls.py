from django.urls import path

from .views import IndexView, MapIndexView, MapAdminView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('map/', MapIndexView.as_view(), name='signed'),
    path('mapadmin/', MapAdminView.as_view())
]