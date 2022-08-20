from .serializers import *
from .models import *
from .forms import *

from django.http import Http404
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


# 회원 가입
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "nickname": user.nickname,
                    "message": "Register Succeed",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie('refresh', str(refresh_token), httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    def post(self, request):

        nickname = request.data.get('nickname')
        password = request.data.get('password')

        user = authenticate(nickname=nickname, password=password)

        if user is not None:
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "nickname": user.nickname,
                    "message": "Login Succeed",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )
            res.set_cookie('refresh', str(refresh_token), httponly=True)

            return res

        else:
            return Response({"message": "Login Failed"}, status=status.HTTP_401_UNAUTHORIZED)