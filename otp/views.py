from django.shortcuts import render
from django.contrib.auth.models import User

import traceback
import random

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def home_page(request):
    return Response(request.user, status=status.HTTP_200_OK)


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

        user = User.objects.create(
            username=username, email=email, password=password
        )
        return Response(
            {"message": f"User registered successfully for {user.username}!"}, status=status.HTTP_201_CREATED
        )
    except:
        print(traceback.format_exception)
        return Response(status=status.HTTP_409_CONFLICT)
