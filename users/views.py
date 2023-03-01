from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import LoginForm, RegisterForm, ActivateForm

# Create your views here.

User = get_user_model()


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST or None)

        if form.is_valid():

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('/')

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save()

            return redirect("users:activate", slug=user.slug)

    context = {
        "form": form
    }
    return render(request, "accounts/register.html", context)



def account_activate_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = ActivateForm()

    if request.method == "POST":
        form = ActivateForm(request.POST or None)

        if form.is_valid():
            form.save(user=user)
            # login(request, user)
            return redirect('users:login')


    context = {
        "form": form
    }
    return render(request, "accounts/activate.html", context)
