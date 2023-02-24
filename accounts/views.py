from django.shortcuts import render, redirect
from .models import User, Profile
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/accounts/login/")

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")
