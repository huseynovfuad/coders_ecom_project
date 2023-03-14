from rest_framework import generics
from .serializers import (
    LoginSerializer, RegisterSerializer, ActivationSerializer
)
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()



class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=201)



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class ActivationView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ActivationSerializer
    lookup_field = "slug"

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = {}
        if obj.activation_code == request.data.get("code"):
            obj.is_active = True
            obj.activation_code = None
            obj.save()
            token = RefreshToken.for_user(obj)
            data["email"] = obj.email
            data["token"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=201)
        else:
            return Response({"error": "Wrong code"})