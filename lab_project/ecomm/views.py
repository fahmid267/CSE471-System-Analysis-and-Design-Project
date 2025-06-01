from django.shortcuts import render, get_object_or_404
from .models import Product, Reviews
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.

def index(request):
    product = Product.objects.all()

    return render(request, "index.html", {"product": product})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    products = Product.objects.filter(type = product.type)
    rev = Reviews.objects.filter(product = product)
    user = request.user

    if product.type == "Shoes":
        sizes = ["40", "41", "42", "43"]

        if product.category == "Boys" or product.category == "Girls":
            sizes = ["32", "33", "34", "35"]
    else:
        sizes = ["S", "M", "L", "XL"]
    
    context = {"product": product, "products": products, "rev" : rev, "user" : user, "sizes" : sizes}
    
    return render(request, "product_detail.html", context)




@login_required
def reviews(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    # rev, created = Reviews.objects.get_or_create(product_id = product_id)

    if request.method == "POST":
        review_text = request.POST.get("review")

        if review_text:
            Reviews.objects.create(product_id = product_id, user = request.user, review_box = review_text)
    
    rev = Reviews.objects.filter(product = product)

    user = request.user
    

    return render(request, "product_detail.html", {"rev" : rev, "product" : product})


def products_by_type(request, type, category):
    type = type.replace('-', ' ')
    category = category.replace('-', ' ')

    products = Product.objects.filter(type = type, category = category) 

    return render(request, 'products_by_type.html', {'products': products, 'type': type, 'category': category})


def products_by_type(request, type, category, name=None):
    type = type.replace('-', ' ')
    category = category.replace('-', ' ')

    products = Product.objects.filter(type=type, category=category)

    if name:
        products = products.filter(name__icontains=name)

    return render(request, 'products_by_type.html', {'products': products, 'type': type, 'category': category})