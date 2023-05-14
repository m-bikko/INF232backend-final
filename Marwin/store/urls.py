from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('search/', views.searchBar, name='search'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('addToCart/', views.add_to_cart, name='atc')
]
