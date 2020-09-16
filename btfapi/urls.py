from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.LinkViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('read-link', views.read_link),
    path('create-link', views.create_link)
]
