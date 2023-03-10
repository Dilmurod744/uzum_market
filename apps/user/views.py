from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt import views

from apps.user import models, serializers
from apps.user.models import User
from apps.user.permissions import IsOwner
from apps.user.serializers import UserSerializer, ClientModelSerializer, MerchantModelSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, IsOwner)


class LoginView(views.TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UpdateUserSerializer


class ClientModelViewSet(ModelViewSet):
    queryset = User.objects.filter(type=User.Type.CLIENT)
    serializer_class = ClientModelSerializer
    # permission_classes = (IsAdminUserOrReadOnly,)


class MerchantModelViewSet(ModelViewSet):
    queryset = User.objects.filter(type=User.Type.MERCHANT)
    serializer_class = MerchantModelSerializer
    permission_classes = (IsAuthenticated, IsOwner)
