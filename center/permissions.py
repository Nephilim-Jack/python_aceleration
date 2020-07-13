from .models import User
from rest_framework.permissions import BasePermission


class HasToken(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        if 'user' in request.headers and 'token' in request.headers:
            pass
        else:
            return False
        usersData = [(user.username, user.token)
                     for user in User.objects.all()]
        return (request.headers['user'], request.headers['token']) in usersData
