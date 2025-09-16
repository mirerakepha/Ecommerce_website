"""
URL configuration for ecommercewebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from ecommercewebsite import settings
from shopapp import views
from django.contrib.auth import views as auth_views
from ecommercewebsite import settings
from ecommercewebsite.settings import MEDIA_ROOT
from django.contrib import admin
from django.urls import path
from shopapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_user, name='login'),
    path("login/", views.logout_user, name='login'),
    path("about/", views.about, name='about'),
    path("cart/", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
    path("notifications/", views.notifications, name='notifications'),
    path("payment/", views.payment, name='payment'),
    path("profile/", views.profile, name='profile'),
    path("product_details/", views.product_details, name='product_details'),
    path("settings/", views.settings, name='settings'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('search/', views.search_results, name='search_results'),
    path("category/<str:category_name>/", views.category, name="category"),
    path("categories/", views.categories, name="categories"),
]
