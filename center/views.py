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
        del form.fields['username']
        context = {
            'form': form,
            'alert': True
        }
        return render(request, 'center/initpages/login.html', context=context)

    return render(request, 'center/initpages/login.html', context=context)


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
            return render(request, 'center/initpages/login.html', context=context)
    return render(request, 'center/initpages/register.html', context=context)


def eventsPage(request):
    try:
        if request.session['username'] == '':
            raise Exception('Invalid Session Data')
        if request.session['token'] == '':
            raise Exception('Invalid Session Data')
    except:
        return redirect('center:loginPage')

    requestParams = False
    try:
        showOnly = request.GET.get('showOnly')
        orderBy = request.GET.get('orderBy')
        findBy = request.GET.get('findBy')
        query = request.GET.get('q')

        if all(showOnly, orderBy, findBy, query):
            requestParams = True
    except:
        pass

    # filtering

    events = Event.objects.all()
    if requestParams:
        if showOnly != 'A':
            events = events.filter(findWhere__exact=showOnly)
        if findBy != 'A':
            if findBy == 'L':
                events = events.filter(level__contains=query)

            if findBy == 'D':
                events = events.filter(details__contains=query)

            if findBy == 'O':
                events = events.filter(findWhere__contains=query)

        if orderBy != 'A':
            if orderBy == 'L':
                events = events.order_by('level')
            if orderBy == 'F':
                events = events.order_by('-quantity')

    eventsSerialized = list()
    for event in events:
        if event.level == 'C':
            event.level = 'Critical'
        elif event.level == 'D':
            event.level = 'Debug'
        elif event.level == 'E':
            event.level = 'Error'
        elif event.level == 'I':
            event.level = 'Information'
        elif event.level == 'W':
            event.level = 'Warning'

        if event.findWhere == 'D':
            event.findWhere = 'Desenvolvimento'
        elif event.findWhere == 'H':
            event.findWhere = 'Homologação'
        elif event.findWhere == 'P':
            event.findWhere = 'Produção'

        eventsSerialized.append(event)
    context = {
        'user': User.objects.get(token__exact=request.session['token']),
        'events': eventsSerialized
    }
    return render(request, 'center/eventPages/list.html', context=context)


def detailEvent(request, eventPk):
    try:
        if request.session['username'] == '':
            raise Exception('Invalid Session Data')
        if request.session['token'] == '':
            raise Exception('Invalid Session Data')
    except:
        return redirect('center:loginPage')

    event = Event.objects.get(pk=eventPk)

    if event.level == 'C':
        event.level = 'Critical'
    elif event.level == 'D':
        event.level = 'Debug'
    elif event.level == 'E':
        event.level = 'Error'
    elif event.level == 'I':
        event.level = 'Information'
    elif event.level == 'W':
        event.level = 'Warning'

    user = User.objects.get(token__exact=request.session['token'])
    context = {
        'event': event,
        'user': user,
    }
    return render(request, 'center/eventPages/detail.html', context=context)


def deleteEvent(request, eventPk):
    try:
        if request.session['username'] == '':
            raise Exception('Invalid Session Data')
        if request.session['token'] == '':
            raise Exception('Invalid Session Data')
    except:
        return redirect('center:loginPage')

    Event.objects.get(pk=eventPk).delete()
    return redirect('center:eventsPage')


def fileEvent(request, eventPk):
    try:
        if request.session['username'] == '':
            raise Exception('Invalid Session Data')
        if request.session['token'] == '':
            raise Exception('Invalid Session Data')
    except:
        return redirect('center:loginPage')

    event = Event.objects.get(pk=eventPk)
    if event.filed:
        event.filed = False
    else:
        event.filed = True
    event.save()
    return redirect('center:eventsPage')


def logOut(request):
    request.session.flush()
    return redirect('center:loginPage')
