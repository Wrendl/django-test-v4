from django.urls import path
from . import views
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserProfileListCreateView

urlpatterns = [
    path('', views.index, name='index'),

    path('sign-up/', UserViewSet.as_view({'post': 'create'}), name="sign-up"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path('profile/', UserViewSet.as_view({'get': 'me', 'patch': 'me'}), name="profile"),

    path("activation/", UserViewSet.as_view({"post": "activation"}), name="activate"),
    path("activate/<str:uid>/<str:token>/", views.confirm, name="confirm_account"),

    path("reset-password/", UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path("reset-password-confirm/", UserViewSet.as_view({"post": "reset_password_confirm"}), name="reset_password_confirm"),
    path("password/reset/confirm/<str:uid>/<str:token>/", views.reset_password, name="reset_password_confirm"),

    # path('private/', views.private, name='private'),
    path("all-profiles/", UserProfileListCreateView.as_view(), name="all-profiles"),
]
