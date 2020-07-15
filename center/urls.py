from django.urls import path, include
from rest_framework import routers
from .views import (
    EventViewSet, UserViewSet,
    registerPage, loginPage,
    eventsPage, logOut, fileEvent,
    deleteEvent, detailEvent
)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', loginPage, name='loginPage'),
    path('register', registerPage, name='register'),
    path('logout', logOut, name='logOutPage'),
    path('events', eventsPage, name='eventsPage'),
    path('events/<int:eventPk>', detailEvent, name='detailEvent'),
    path('events/<int:eventPk>/fileEvent', fileEvent, name='fileEvent'),
    path('events/<int:eventPk>/deleteEvent', deleteEvent, name='deleteEvent'),
    path('api/', include(router.urls))
]
