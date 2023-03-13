from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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

        user = User.objects.create(email=email, full_name=full_name)
        user.set_password(password)
        user.save()
        return user


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["token"] = {"refresh": str(token), "access": str(token.access_token)}
        return repr_
