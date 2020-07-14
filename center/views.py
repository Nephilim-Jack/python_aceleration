from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
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


def loginPage(request):
    if request.method == 'GET':
        try:
            if request.session['username'] == '':
                raise Exception('Invalid Session Data')
            if request.session['token'] == '':
                raise Exception('Invalid Session Data')

            return redirect('center:eventsPage')
        except:
            pass
        form = UserModelForm()
        del form.fields['username']
        context = {
            'form': form
        }
    else:
        form = UserModelForm(request.POST)
        form.is_valid()

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        for user in User.objects.filter(email__exact=email):
            if check_password(password, user.password):
                request.session['username'] = user.username
                request.session['token'] = user.token
                return redirect('center:eventsPage')

        form = UserModelForm()
        context = {
            'form': form,
            'alert': True
        }
        return render(request, 'initpages/login.html', context=context)

    return render(request, 'initpages/login.html', context=context)


def registerPage(request):
    if request.method == 'GET':
        context = {
            'form': UserModelForm()
        }
    else:
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()

            users = User.objects.filter(
                username__exact=form.cleaned_data['username'],
                email__exact=form.cleaned_data['email']
            )
            for user in users:
                if check_password(form.cleaned_data['password'], user.password):
                    request.session['username'] = user.username
                    request.session['token'] = user.token
            return redirect('center:eventsPage')
        else:
            context = {
                'form': form,
            }
            return render(request, 'initpages/login.html', context=context)
    return render(request, 'initpages/register.html', context=context)


def eventsPage(request):
    try:
        if request.session['username'] == '':
            raise Exception('Invalid Session Data')
        if request.session['token'] == '':
            raise Exception('Invalid Session Data')
    except:
        return redirect('center:loginPage')
    context = {
        'userToken': request.session['token']
    }
    return render(request, 'eventPages/list.html', context=context)


def logOut(request):
    request.session.flush()
    return redirect('center:loginPage')
