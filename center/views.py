from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, mixins
from .models import Event, User
from .serializers import EventSerializer, UserSerializer
from .permissions import HasToken
from .forms import UserModelForm

# Create your views here.


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (HasToken, )
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def registerPage(request):
    if request.method == 'GET':
        context = {
            'form': UserModelForm()
        }
    else:
        # validate
        pass
    return render(request, 'initpages/register.html', context=context)
