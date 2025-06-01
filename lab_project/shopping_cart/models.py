from django.db import models
from django.conf import settings
from ecomm.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    # products = models.ManyToManyField(Product, through = "CartItem")
    checked_out = models.BooleanField(default = False)
    total_price = models.FloatField(default = 0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    price = models.FloatField(default = 0)
    quantity = models.PositiveIntegerField(default = 0)
    product_name = models.TextField(max_length = 100)
    product_img = models.ImageField()
    product_size = models.TextField()