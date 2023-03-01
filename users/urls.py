from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register_view, name="register"),
    path("activate/<slug>/", views.account_activate_view, name="activate"),
]