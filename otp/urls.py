from django.urls import path
from .views import home_page, register_user, login_user

urlpatterns = [
    path("home/", home_page, name="home"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
]
