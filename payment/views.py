from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


# Create your views here.
def checkout(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    cart_products = cart.get_prods()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #checkout as logged in user
        shipping_user = ShippingAddress.objects.get(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html',{'cart_products': cart_products, 'quantities': quantities, 'cart': cart, 'totals': totals, 'shipping_form': shipping_form})
    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'checkout.html',{'cart_products': cart_products, 'quantities': quantities, 'cart': cart, 'totals': totals, 'shipping_form': shipping_form})







def payment_success(request):
    return render(request, 'payment_success.html')