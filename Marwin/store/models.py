from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    prices = models.FloatField(null=True, blank=True)
    descript = models.CharField(max_length=1000, null=True)
    image = models.ImageField(null=True, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.prices * self.quantity
        return total


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(default='John Doe (Default)', max_length=200, null=True)
    title = models.CharField(default='Bla Bla Bla....', max_length=200, null=True)
    desc_text = 'Bla Bla Bla.....'
    phone = models.CharField(max_length=12)
    descript = models.CharField(default=desc_text, max_length=200, null=True)
    profile_img = models.ImageField(default='media/default.jpg', upload_to='media', null=True, blank=True)

    def __str__(self):
        return self.name
