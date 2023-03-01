# from django.shortcuts import render, redirect, get_object_or_404
# from .models import User, Profile
# from .forms import LoginForm, RegisterForm
# from django.contrib.auth import authenticate, login, logout
# from django.core.mail import send_mail
# from services.generator import CodeGenerator
# from django.conf import settings
# from django.urls import reverse_lazy
#
# # Create your views here.
#
#
# def login_view(request):
#     form = LoginForm()
#
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect("/accounts/login/")
#
#     context = {
#         "form": form
#     }
#     return render(request, "accounts/login.html", context)
#
#
# def logout_view(request):
#     logout(request)
#     return redirect("/")
#
#
#
# def register_view(request):
#     print(request.user)
#     form = RegisterForm()
#
#     if request.method == "POST":
#         form = RegisterForm(request.POST or None)
#
#         if form.is_valid():
#             new_user = form.save(commit=True)
#             new_user.is_active = False
#             password = form.cleaned_data.get("password")
#             new_user.set_password(password)
#             new_user.save()
#             # profile = Profile.objects.create(
#             #     user=new_user,
#             #     activation_code=CodeGenerator.create_activation_link_code(
#             #         size=30, model_=Profile
#             #     )
#             # )
#             profile = Profile.objects.create(
#                 user=new_user,
#                 activation_code=CodeGenerator.create_activation_link_code(
#                     size=4, model_=Profile
#                 )
#             )
#             # link = request.build_absolute_uri(f'/accounts/activate/account/{profile.activation_code}/')
#
#             message = f"Please write code below: \n{profile.activation_code}"
#
#             # sending mail
#             send_mail(
#                 'Activate email', # subject
#                 message, # message
#                 settings.EMAIL_HOST_USER, # from email
#                 [new_user.email], # to mail list
#                 fail_silently=False,
#             )
#
#             return redirect(reverse_lazy("accounts:activate", kwargs={"slug": profile.slug}))
#
#     context = {
#         "form": form
#     }
#     return render(request, "accounts/register.html", context)
#
#
#
# def activate_account_view(request, activation_code):
#     profile = get_object_or_404(Profile, activation_code=activation_code)
#     profile.user.is_active = True
#     profile.activation_code = None
#     profile.user.save()
#     profile.save()
#     login(request, profile.user)
#     return redirect('/')
#
#
#
#
# def activate_account_code_view(request, slug):
#     profile = get_object_or_404(Profile, slug=slug)
#
#     if request.method == "POST":
#         code = request.POST.get("code")
#
#         if code == profile.activation_code:
#             profile.user.is_active = True
#             profile.activation_code = None
#             profile.user.save()
#             profile.save()
#             login(request, profile.user)
#             return redirect('/')
#     return render(request, "accounts/activate.html", {})