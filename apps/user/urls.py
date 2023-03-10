from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from apps.user.views import LoginView, RegisterView, ChangePasswordView, UpdateProfileView

router = routers.DefaultRouter()

urlpatterns = [
    re_path(r'^login/', LoginView.as_view(), name='auth_login'),
    re_path(r'^login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^logout/', TokenBlacklistView.as_view(), name='auth_logout'),
    re_path(r'^register/', RegisterView.as_view(), name='auth_register'),

    re_path(r'^change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    re_path(r'^update_account/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),

    path('', include(router.urls)),
]
