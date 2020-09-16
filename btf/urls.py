from django.urls import include, path

from . import views

urlpatterns = [
    path('create', views.create_link),
    path('<slug:code>', views.read_link),
]
