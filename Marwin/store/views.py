from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def store(request):
    context = {}
    return render(request, 'store/Main.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'{username},You are logged in.')
            return redirect("store")
        else:
            messages.info(request, 'Wrong username or password')
            return redirect('login')
    return render(request, 'store/log.html')


def register_user(request):
    context = {}
    return render(request, 'store/sign.html')
