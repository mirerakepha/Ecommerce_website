from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from .forms import UserForm, ProfileForm
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token

from .forms import SignupForm, LoginForm


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = SignupForm()
            return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login_view(request, user)
            return redirect('home')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})


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