from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect

from cart import models
from cart.cart import Cart
from shopapp.models import Product, Profile
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required


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

            #delete/empty cart items after order has been processed->deleting the session # in carts.py its called the session_key
            if 'session_key' in request.session:
                del request.session['session_key']
                request.session.modified = True

            #delete cart from the database after processing orders(old cart)
            if request.user.is_authenticated:
                profile = Profile.objects.filter(user=request.user).first()
                if profile:
                    profile.old_cart = ""  # empty cart in db
                    profile.save()


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


@login_required
def shipped_dash(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access Denied.')
        return redirect('home')

    if request.method == "POST":
        order_id = request.POST.get("num")
        Order.objects.filter(id=order_id).update(shipped=False)
        messages.success(request, f"Order #{order_id} marked as NOT shipped.")
        return redirect("shipped_dash")

    orders = Order.objects.filter(shipped=True)
    return render(request, 'shipped_dash.html', {'orders': orders})


@login_required
def not_shipped_dash(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access Denied.')
        return redirect('home')

    if request.method == "POST":
        order_id = request.POST.get("num")
        Order.objects.filter(id=order_id).update(shipped=True)
        messages.success(request, f"Order #{order_id} marked as shipped.")
        return redirect("not_shipped_dash")

    orders = Order.objects.filter(shipped=False)
    return render(request, 'not_shipped_dash.html', {'orders': orders})


@login_required
def orders(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Access Denied.')
        return redirect('home')

    order = Order.objects.get(id=pk)
    items = order.items.all()

    if request.method == "POST":
        status = request.POST.get('shipping_status')
        order.shipped = (status == "true")
        order.save()#save shipping status
        messages.success(request, "Shipping status updated!")

        if order.shipped:
            return redirect('shipped_dash')
        else:
            return redirect('not_shipped_dash')

    return render(request, 'orders.html', {"order": order, "items": items})
