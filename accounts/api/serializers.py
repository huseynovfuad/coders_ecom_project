from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from services.generator import CodeGenerator
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("email", "password")



    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "This email does not exist"})
        if not user:
            raise serializers.ValidationError({"error": "Email or password are wrong"})
        if not user.is_active:
            raise serializers.ValidationError({"error": "This user is not active"})

        return attrs

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        user = User.objects.get(email=instance.get("email"))
        token = RefreshToken.for_user(user)
        repr_["token"] = {"refresh": str(token), "access": str(token.access_token)}
        return repr_




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("email", "full_name", "password", "password_confirm")


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "This email already exists"})

        if password != password_confirm:
            raise serializers.ValidationError({"error": "Passwords don't match"})

        return attrs

    def create(self, validated_data):
        email = validated_data.get("email", None)
        full_name = validated_data.get("full_name", None)
        password = validated_data.get("password", None)

        user = User.objects.create(
            email=email, full_name=full_name, is_active=False,
            activation_code=CodeGenerator.create_activation_link_code(size=6, model_=User)
        )
        user.set_password(password)
        user.save()

        # sending mail
        message = f"Please write code below: \n{user.activation_code}"
        send_mail(
            'Activate email', # subject
            message, # message
            settings.EMAIL_HOST_USER, # from email
            [user.email], # to mail list
            fail_silently=False,
        )

        return user


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["slug"] = instance.slug
        return repr_


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField()