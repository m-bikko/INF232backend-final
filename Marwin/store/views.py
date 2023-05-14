from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm, ProfileForm
from .models import *


# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


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
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Account is create.')
            return redirect('login')
        else:
            context = {'form': form}
            messages.info(request, 'Invalid Invalid')
            return render(request, 'store/register_page.html', context)
    context = {'form': form}
    return render(request, 'store/sign.html', context)


def searchBar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__contains=query)
            return render(request, 'store/searchBar.html', {'products': products})
        else:
            print("No information show")
            return render(request, 'store/searchBar.html', {})


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username},Your profile is update.')
            return redirect('/')
    else:
        form = ProfileForm(instance=request.user.profile)
    contex = {'form': form}
    return render(request, 'store/profile.html',contex)


def logout_user(request):
    logout(request)
    messages.info(request, 'You  logged out successfully')
    return render(request, 'store/log.html')
