from django.contrib import messages
from django.shortcuts import render, redirect

from cart import models
from cart.cart import Cart
from shopapp.models import Product
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


# Create your views here.
def checkout(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    cart_products = cart.get_prods()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Try to get shipping address, or None if not exists
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()

        if shipping_user:
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        else:
            shipping_form = ShippingForm(request.POST or None)

        return render(request, 'checkout.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'cart': cart,
            'totals': totals,
            'shipping_form': shipping_form
        })

    else:
        # checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'checkout.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'cart': cart,
            'totals': totals,
            'shipping_form': shipping_form
        })



from types import SimpleNamespace

def billing_info(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    cart_products = cart.get_prods()
    totals = cart.cart_total()

    shipping_info = None

    if request.method == "POST":
        billing_form = PaymentForm(request.POST or None)
        shipping_form = ShippingForm(request.POST or None)

        if shipping_form.is_valid():
            request.session['my_shipping'] = shipping_form.cleaned_data
            # Convert dict to object
            shipping_info = SimpleNamespace(**shipping_form.cleaned_data)
        else:
            messages.error(request, "Invalid shipping information")

        if request.user.is_authenticated:
            return render(request, 'billing_info.html', {
                'cart_products': cart_products,
                'quantities': quantities,
                'cart': cart,
                'totals': totals,
                'billing_form': billing_form,
                'shipping_form': shipping_form,
                'shipping_info': shipping_info or None
            })
        else:
            messages.error(request, 'You must be logged in to continue.')
            return redirect('login')

    else:
        data = request.session.get('my_shipping', None)
        if data:
            shipping_info = SimpleNamespace(**data)

        billing_form = PaymentForm()
        shipping_form = ShippingForm()

        return render(request, 'billing_info.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'cart': cart,
            'totals': totals,
            'billing_form': billing_form,
            'shipping_form': shipping_form,
            'shipping_info': shipping_info
        })


def process_order(request):
    if request.method == "POST":
        cart = Cart(request)
        quantities = cart.get_quants()
        cart_products = cart.get_prods()
        totals = cart.cart_total()

        # validate payment form
        payment_form = PaymentForm(request.POST)
        my_shipping = request.session.get('my_shipping')

        if not my_shipping:
            messages.error(request, "No shipping information found. Please enter shipping first.")
            return redirect('checkout')

        if payment_form.is_valid():
            # extract shipping info
            full_name = my_shipping.get('shipping_fullname')
            email = my_shipping.get('shipping_email')
            shipping_address = f"{my_shipping.get('shipping_street')}\n{my_shipping.get('shipping_country')}\n{my_shipping.get('shipping_city')}\n{my_shipping.get('shipping_state')}\n{my_shipping.get('shipping_zipcode')}"

            amount_paid = totals

            # create order
            if request.user.is_authenticated:
                user = request.user
                create_order = Order(
                    user=user,
                    fullname=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=amount_paid
                )
            else:
                user = None  # guest
                create_order = Order(
                    fullname=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=amount_paid
                )

            create_order.save()

            # add order items
            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.on_sale else product.price

                # get quantity for this product
                quantity = quantities.get(str(product_id)) or quantities.get(product_id)
                if quantity:
                    create_order_item = OrderItem(
                        order=create_order,
                        user=user,
                        product=product,
                        quantity=quantity,
                        price=price
                    )
                    create_order_item.save()

            messages.success(request, "Order created successfully!")
            return redirect('home')

        else:
            messages.error(request, "Invalid payment details. Please check your input.")
            return redirect('billing_info')

    else:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')



def payment_success(request):
    return render(request, 'payment_success.html')