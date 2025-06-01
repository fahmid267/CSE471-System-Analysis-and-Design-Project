import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Create your views here.

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    user = request.user

    size = request.POST.get('size', "")

    cart, created = Cart.objects.get_or_create(user = user)
    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product, product_size = size)

    cart_item.product_name = product.name
    cart_item.product_img = product.img
    cart_item.quantity += 1
    cart_item.price += product.price
    cart_item.product_size = size

    cart.total_price += product.price

    cart_item.save()
    cart.save()

    messages.info(request, "Added to Cart!")

    return redirect("product_detail", product_id = product_id)

# @login_required
def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user = user)
    cart_items = CartItem.objects.filter(cart = cart)

    if not cart_items:
        messages.info(request, "Your cart is currently empty")

    return render(request, 'cart.html', {"cart_items" : cart_items, "cart" : cart})

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id = item_id)
    user = request.user
    product = Product.objects.get(id = cart_item.product_id)
    cart = cart_item.cart

    if request.POST.get('qty-add'):
        cart_item.quantity += 1
    elif request.POST.get('qty-sub'):
        cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
            
            cart_items = CartItem.objects.filter(cart = cart)
            cart.total_price = sum(item.price for item in cart_items)
            
            cart.save()

            return redirect('view_cart')
    
    cart_item.price = (product.price * cart_item.quantity)

    cart_item.save()

    cart_items = CartItem.objects.filter(cart = cart)

    cart.total_price = sum(item.price for item in cart_items)
    cart.save()
    
    return redirect('view_cart')


def download_invoice(request):
    try:
        cart = Cart.objects.get(user=request.user)

        cart_items = list(CartItem.objects.filter(cart=cart))
        total_price = cart.total_price

        html = render_to_string('invoice_template.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'user': request.user,
        })

        
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

        if not pdf.err:
            
            pdf_name = f"invoice_{request.user.id}.pdf"
            file_path = default_storage.save(pdf_name, ContentFile(result.getvalue()))

            
            CartItem.objects.filter(cart=cart).delete()
            cart.total_price = 0
            cart.save()

            
            request.session['invoice_path'] = file_path  
            return HttpResponseRedirect(reverse('purchase_completed'))
        else:
            return HttpResponse('Error generating PDF')
    except Cart.DoesNotExist:
        return HttpResponse('No cart found for this user')

def purchase_completed(request):
    return render(request, 'purchase_completed.html')

def download_invoice_file(request):

    file_path = request.session.get('invoice_path')

    if file_path and default_storage.exists(file_path):
        with default_storage.open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="invoice.pdf"'
            return response
    else:
        return HttpResponse('Invoice not available')