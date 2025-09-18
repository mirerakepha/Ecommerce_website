from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shopapp.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    cart_products = cart.get_prods()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'cart': cart, 'totals': totals })


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))#this gets that stuff from the dropdown ti select the quantity
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)#account for the quantity in the cart.py
        #cart quantity
        cart_quantity = cart.__len__()
        #response
        response = JsonResponse({'qty': cart_quantity })
        messages.success(request, "Item added to cart")
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product_id=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        # pass product_id directly
        cart.delete(product_id)

        response = JsonResponse({'product': product_id})
        return response