from django.urls import path
from .views import home_page, register_user, login_user, send_otp, check_otp

urlpatterns = [
    path("home/", home_page, name="home"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("send-otp/", send_otp, name="send-otp"),
    path("check-otp/", check_otp, name="check-otp"),
]
