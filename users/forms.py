from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from services.generator import CodeGenerator
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

# -----------------------   Admin Forms  ---------------------------------------------------


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "password1",
            "password2",
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "is_active",
            "is_superuser",
            "password",
        ]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]




# Login Form

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError("This user does not exists")

        if not user.is_active:
            raise forms.ValidationError("This user is not active")

        if not user.check_password(password):
            raise forms.ValidationError("Email or password is wrong")

        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })


class RegisterForm(UserAdminCreationForm):

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save()
        user.set_password(self.cleaned_data.get("password1"))
        user.is_active = False
        user.activation_code = CodeGenerator.create_activation_link_code(
            size=4, model_=User
        )
        if commit:
            user.save()

        message = f"Please write code below: \n{user.activation_code}"

        # send mail
        send_mail(
            'Activate email', # subject
            message, # message
            settings.EMAIL_HOST_USER, # from email
            [user.email], # to mail list
            fail_silently=False,
        )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })



class ActivateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("activation_code", )


    def save(self, user):
        activation_code = self.cleaned_data.get("activation_code")

        if activation_code == user.activation_code:
            user.is_active = True
            user.activation_code = None
            user.save()
        else:
            raise forms.ValidationError("Kod duzgun deyil")


        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })



class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})



class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email does not exist")
        return self.cleaned_data



class ResetPasswordCompleteForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if len(password1.strip()) < 6:
            raise forms.ValidationError("Duzgun kod yaz")

        if password1 != password2:
            raise forms.ValidationError("Passwords dont match")

        return self.cleaned_data


    def save(self):
        password1 = self.cleaned_data.get("password1")
        self.instance.set_password(password1)
        self.instance.save()
        return self.instance