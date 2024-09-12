from django.shortcuts import render
from django.contrib.auth.models import User

from .models import OTPCode

import traceback
import random

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def home_page(request):
    return Response({"Message": f"Welcome {request.user}!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response(
                {"error": "Username, Password and email are required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists!!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(username=username, email=email, password=password)
        Token.objects.create(user=user)
        return Response(
            {"message": f"User registered successfully for {user.username}!"},
            status=status.HTTP_201_CREATED,
        )
    except:
        print(traceback.format_exception)
        return Response(status=status.HTTP_409_CONFLICT)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_user(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {"error": "email, and password are required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not User.objects.filter(email=email, password=password).exists():
            return Response(
                {"error": "Username or password are incorrect!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.get(email=email, password=password)
        token = Token.objects.get(user=user)

        return Response({"token": {token.key}})
    except:
        print(traceback.format_exception)
        return Response(status=status.HTTP_409_CONFLICT)


def create_otp(phone, is_new=True):
    otp_code = random.randint(1000, 9999)
    if is_new:
        OTPCode.objects.create(phone=phone, code=otp_code)
    else:
        old_OTPCode = OTPCode.objects.get(phone=phone)
        old_OTPCode.code = otp_code
        old_OTPCode.save()
    return otp_code


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def send_otp(request):
    try:
        phone = request.data.get("phone")

        if not phone:
            return Response(
                {"error": "Phone number is required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if OTPCode.objects.filter(phone=phone).exists():
            otp_code = create_otp(phone, is_new=False)
        else:
            otp_code = create_otp(phone, is_new=True)

        # emulate sending otp
        print(otp_code)
        return Response(
            {"message": "OTP send to your phone!"}, status=status.HTTP_200_OK
        )

    except:
        print(traceback.format_exception)
        return Response(status=status.HTTP_409_CONFLICT)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def check_otp(request):
    try:
        phone = request.data.get("phone")
        otp_code = request.data.get("otp")

        if not phone or not otp_code:
            return Response(
                {"error": "Phone number, and otp are required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not OTPCode.objects.filter(phone=phone).exists():
            return Response(
                {"error": "phone isn't registered!"}, status=status.HTTP_400_BAD_REQUEST
            )

        stored_otp = OTPCode.objects.get(phone=phone)
        if stored_otp.code == otp_code:
            return Response(
                {"message": "Verification Completed!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "OTP code doesn't match, Verification failed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except:
        print(traceback.format_exception)
        return Response(status=status.HTTP_409_CONFLICT)
