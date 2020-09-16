from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('btfapi/', include('btfapi.urls')),
    path('', include('btf.urls')),
    path('', views.index)
]
