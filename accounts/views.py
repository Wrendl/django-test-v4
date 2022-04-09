from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import UserAccount
from .serializers import UserCreateSerializer


def index(request):
    return render(request, 'accounts/index.html')


def confirm(request, uid, token):
    if request.method == 'GET':
        return render(request, 'accounts/confirm.html', {'uid': uid, 'token': token})


def private(request):
    return render(request, 'accounts/private.html')


class UserProfileListCreateView(ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]
