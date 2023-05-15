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


def add_quantity(request):
    if request.method == 'POST':
        order_item = OrderItem.objects.get(pk=request.POST['oi'])
        order_item.quantity += 1
        order_item.save()
        return redirect('cart')
    else:
        return redirect('store')


def del_quantity(request):
    if request.method == 'POST':
        order_item = OrderItem.objects.get(pk=request.POST['oi'])
        order_item.quantity -= 1
        if order_item.quantity > 0:
            order_item.save()
        else:
            order_item.delete()
        return redirect('cart')
    else:
        return redirect('store')


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()
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
        if OrderItem.objects.filter(product=product, order=order):
            messages.info(request, 'This product already added to cart')
            return redirect('store')
        else:
            OrderItem.objects.create(product=product, order=order)
            return redirect('cart')
    else:
        return redirect('store')


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
            print(form)
            user = form.save(commit=False)
            user.save()
            login(request, user)
            customer = Customer.objects.create(user=user, name=user.username, email=user.email)
            Order.objects.create(customer=customer)
            messages.info(request, 'Account is create.')
            return redirect('store')
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
    return render(request, 'store/profile.html', contex)


def logout_user(request):
    logout(request)
    messages.info(request, 'You  logged out successfully')
    return render(request, 'store/log.html')


def productView(request, product_id):
    product = Product.objects.get(pk=product_id)
    recently_viewed_products = None

    if 'recently_viewed' in request.session:
        if product_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(product_id)

        products = Product.objects.filter(pk__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(products,
                                          key=lambda x: request.session['recently_viewed'].index(x.id)
                                          )
        request.session['recently_viewed'].insert(0, product_id)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [product_id]

    request.session.modified = True

    contex = {'product': product, 'recently_viewed_products': recently_viewed_products}
    return render(request, 'store/prodView.html', contex)


def productinf(request, product_id):
    product = Product.objects.get(pk=product_id)
    recently_viewed_products = None

    if 'recently_viewed' in request.session:
        if product_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(product_id)

        products = Product.objects.filter(pk__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(products,
                                          key=lambda x: request.session['recently_viewed'].index(x.id)
                                          )
        request.session['recently_viewed'].insert(0, product_id)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [product_id]

    request.session.modified = True

    contex = {'product': product, 'recently_viewed_products': recently_viewed_products}
    return render(request, 'store/productinf.html', contex)
