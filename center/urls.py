from django.urls import path, include
from rest_framework import routers
from .views import (
    EventViewSet, UserViewSet,
    registerPage, loginPage,
    eventsPage, logOut
)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', loginPage, name='loginPage'),
    path('register', registerPage, name='register'),
    path('logout', logOut, name='logOutPage'),
    path('events', eventsPage, name='eventsPage'),
    path('api/', include(router.urls))
]
