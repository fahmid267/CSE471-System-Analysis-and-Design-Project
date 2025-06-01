from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 100)
    img = models.ImageField(upload_to = "product_img")
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default = False)
    category = models.TextField(max_length = 50)
    type = models.TextField(max_length = 50)

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    review_box = models.TextField(max_length = 500)