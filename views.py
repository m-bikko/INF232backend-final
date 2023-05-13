from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, ProfileForm, PriceFilterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .disable import unauthenticated_user


from .models import *


@login_required(login_url='login')
def store(request):
    products = Product.objects.filter(published=True).all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


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


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def adminPage(request):
    cus = Customer.objects.all()
    contex = {'cus': cus}
    return render(request, 'store/admin.html', contex)


def profAdmin(request):
    prof = Profile.objects.all()
    contex = {'prof': prof}
    return render(request, 'store/profileAdm.html', contex)


def profEdit(request):
    prof = Profile.objects.all()
    context = {
        'prof': prof,
    }
    return render(request, 'store/profileAdm.html')


def updateProf(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        title = request.POST.get('title')
        phone = request.POST.get('phone')
        descript = request.POST.get('descript')

        prof = Profile(
            id=id,
            name=name,
            title=title,
            phone=phone,
            descript=descript
        )
        prof.save()
        return redirect('profAdmin')
    return redirect(request, 'store/profileAdmin.html')


def deleteProf(request, id):
    prof = Profile.objects.filter(id=id)
    prof.delete()
    contex = {
        'prof': prof,
    }
    return redirect('profAdmin')


def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        cus = Customer(
            name=name,
            email=email,
            address=address,
            phone=phone
        )
        cus.save()
        return redirect('adminPage')
    return render(request, 'store/admin.html')


def edit(request):
    cus = Customer.objects.all()
    context = {
        'cus': cus,
    }
    return redirect(request, 'store/admin.html', context)


def update(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        cus = Customer(
            id=id,
            name=name,
            email=email,
            address=address,
            phone=phone
        )
        cus.save()
        return redirect('adminPage')
    return redirect(request, 'store/admin.html')


def delete(request, id):
    cus = Customer.objects.filter(id=id)
    cus.delete()
    contex = {
        'cus': cus,
    }
    return redirect('adminPage')


@login_required(login_url='login')
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


@unauthenticated_user
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

    return render(request, 'store/login_page.html')


@unauthenticated_user
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
    return render(request, 'store/register_page.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.info(request, 'You  logged out successfully')
    return render(request, 'store/login_page.html')


@login_required
def publish_product(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name')
        prices = request.POST.get('price', 0)
        image = request.FILES.get('image')
        Product.objects.create(user=user, name=name, prices=prices, image=image)
        messages.success(request,
                         'Your product has been submitted for review. You will be notified once it is approved.')
        return redirect('publish_product')
    else:
        return render(request, 'store/publish_product.html')


@user_passes_test(lambda u: u.is_superuser)
def manage_products(request):
    products = Product.objects.filter(published=False)

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            products_ids = request.POST.getlist('product_ids')
            for product_id in products_ids:
                product = Product.objects.get(pk=product_id)
                product.published = True
                product.save()
                messages.success(request, f'Product "{product.name}" has been approved and is now published.')

        elif action == 'reject':
            product_ids = request.POST.getlist('product_ids')
            for product_id in product_ids:
                product = Product.objects.get(pk=product_id)
                product.delete()
                messages.warning(request, f'Product "{product.name}" has been rejected and deleted.')
        return redirect('manage_products')

    context = {'products': products}
    return render(request, 'store/manage_products.html', context)


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


def load_products(request):
    product = Product.objects.all()
    contex = {'product': product}
    return render(request, 'store/store.html', contex)


def searchBar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__contains=query)
            return render(request, 'store/tempbar.html', {'products': products})
        else:
            print("No information show")
            return request(request, 'store/tempbar.html', {})


def filterPrice(request):
    if request.method == "POST":
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        products = Product.objects.all()
        if min_price and max_price:
            products = products.filter(prices__range=(float(min_price), float(max_price)))
        elif min_price:
            products = products.filter(prices__gte=float(min_price))
        elif max_price:
            products = products.filter(prices__lte=float(max_price))
    context = {'products': products}
    return render(request, 'store/filter.html', context)
