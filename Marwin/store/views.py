from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from .models import *


# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST['pi'])
        order = Order.objects.get(customer=request.user.customer, complete=False)
        OrderItem.objects.create(product=product, order=order)
        return redirect('cart')

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


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
            user = User.objects.create(**form.cleaned_data)
            customer = Customer.objects.create(user=user, name=user.username, email=user.email)
            Order.objects.create(customer=customer)
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

