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