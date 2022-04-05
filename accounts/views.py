from django.shortcuts import render


def index(request):
    return render(request, 'accounts/index.html')


def index1(request, uid, token):
    return render(request, 'accounts/index1.html', {'uid': uid, 'token': token})
