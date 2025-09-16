from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Profile, Product

from .forms import UserForm, ProfileForm, SignupForm, LoginForm




def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)  # auto login after signup
            messages.success(request, 'You are now registered')
            return redirect("home")
        else:
            messages.error(request, 'problem occurred')
            return redirect("signup")
    else:
        return render(request, "signup.html", {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    else:
        return render(request, "login.html", {'form': LoginForm()})


@require_POST
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")




@login_required
def cart(request):
    return render(request, 'cart.html')


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
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile": profile,
    })


@login_required
def product_details(request):
    return render(request, 'product_details.html')


@login_required
def settings(request):
    return render(request, 'settings.html')




def search_results(request):
    query = request.GET.get("q")
    return render(request, "search_result.html", {"query": query})


def category(request, category_name):
    return render(request, "category.html", {"category_name": category_name})


def categories(request):
    all_categories = ["carpets", "sweats", "officials", "pillows", "duvets", "bags"]
    return render(request, "categories.html", {"categories": all_categories})


def about(request):
    return render(request, "about.html")