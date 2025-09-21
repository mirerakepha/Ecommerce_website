from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Profile, Product, Category, Customer

from .forms import UserForm, ProfileForm, SignupForm, LoginForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db.models import Q #query multiple items using filter
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        #query the database
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #test for null
        if not searched:
            messages.success(request, "Product not found")
            return render(request, "search.html")
        else:
            return render(request, "search.html", {'searched': searched})
    else:
        return render(request, 'search.html', {})


def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)  # auto login after signup
            messages.success(request, 'Account created successfully, fill the extra info')
            return redirect('update_info')
        else:
            messages.error(request, 'Problem occurred')
            return redirect('signup')
    else:
        return render(request, "signup.html", {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #here pull the cart items from the DB  since one needs their items when logged back in
            current_user = Profile.objects.get(user__id=user.id)
            #get the saved cart from db
            saved_cart = current_user.old_cart
            #convert python string back to dictionary
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #add the loaded cart dictionary to out our session and get the cart
                cart = Cart(request=request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, "You are now logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, "login.html", {'form': LoginForm()})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

@login_required
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "Profile has been updated.")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, "You are not logged in.")
        return redirect('login')


@login_required
def update_info(request):
    # Ensure profile exists
    current_user, created = Profile.objects.get_or_create(user=request.user)

    # Ensure shipping address exists
    shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

    # Bind forms
    form = UserInfoForm(request.POST or None, request.FILES or None, instance=current_user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

    if request.method == "POST":
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info has been updated.")
            return redirect('home')

    return render(request, 'update_info.html', {
        'form': form,
        'shipping_form': shipping_form,
    })


@login_required
def checkout(request):
    return render(request, 'checkout.html')


@login_required
def notifications(request):
    return render(request, 'notifications.html')


@login_required
def payment(request):
    return render(request, 'payment.html')


@login_required
def update_user(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("home")
    else:
        form = UpdateUserForm(instance=request.user)

    return render(request, "update_user.html", {"form": form})

def product_details(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product_details.html', {'product': product})


@login_required
def settings(request):
    return render(request, 'settings.html')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = PasswordChangeForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password was successfully updated!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, "Ooops! seems there was an error")
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "You are not logged in.")
        return redirect('home')




def search_results(request):
    query = request.GET.get("q")
    return render(request, "search_result.html", {"query": query})


def categories(request, category_name):
    category_name = category_name.replace('-', ' ')
    try:
        category = Category.objects.get(name__iexact=category_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.error(request, 'Category not found')
        return redirect('categories', category_name=category_name)


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})

def about(request):
    return render(request, "about.html")