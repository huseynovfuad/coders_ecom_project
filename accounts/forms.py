from django import forms
from .models import User, Profile
from django.contrib.auth import authenticate


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "password")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })

    def clean(self):
        attrs = self.cleaned_data

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("This user does not exists")

        if not user.is_active:
            raise forms.ValidationError("This user is not active")

        if not user.check_password(password):
            raise forms.ValidationError("Email or password is wrong")

        return attrs



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "password_confirm")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
    def clean(self):
        attrs = self.cleaned_data

        username = attrs.get("username")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        # user = authenticate(username=username, password=password)
        user_qs = User.objects.filter(username=username)

        if user_qs.exists():
            raise forms.ValidationError("This username already exists")

        if len(password) < 6:
            raise forms.ValidationError("Password must minimum length is 6")

        if password != password_confirm:
            raise forms.ValidationError("Passwords dont match")

        if not password.strip()[0].isalpha():
            raise forms.ValidationError("Password must begin with letter")

        if not password.isalnum():
            raise forms.ValidationError("Password must contain at least 1 number")

        return attrs
