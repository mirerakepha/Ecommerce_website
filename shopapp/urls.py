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
    path("logout/", views.logout_user, name='logout'),
    path("about/", views.about, name='about'),
    path("update_password/", views.update_password, name='update_password'),
    path("notifications/", views.notifications, name='notifications'),
    path("payment/", views.payment, name='payment'),
    path("update_user/", views.update_user, name='update_user'),
    path("update_info/", views.update_info, name='update_info'),
    path("product_details/<int:pk>", views.product_details, name='product_details'),
    path("settings/", views.settings, name='settings'),
    path('search/', views.search, name='search'),
    path("category_summary/", views.category_summary, name="category_summary"),
    path("category/<str:category_name>/", views.categories, name="category"),
]
