from django.urls import path, include
from rest_framework import routers
from .views import (
    EventViewSet, UserViewSet,
    registerPage
)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', registerPage),
    path('api/', include(router.urls))
]
