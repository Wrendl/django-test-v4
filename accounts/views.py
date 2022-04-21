from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import UserAccount
from .serializers import UserCreateSerializer


def index(request):
    return render(request, 'accounts/index.html')


def confirm(request, uid, token):
    return render(request, 'accounts/ConfirmationPage.html', {'uid': uid, 'token': token})
    # return render(request, 'accounts/ConfirmationPage.html')


def reset_password(request, uid, token):
    return render(request, 'accounts/ResetPassword.html', {'uid': uid, 'token': token})


class UserProfileListCreateView(ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserCreateSerializer
