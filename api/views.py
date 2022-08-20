from .serializers import *
from .models import *
from .forms import *

from django.http import Http404
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

import jwt


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


# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.COOKIES.get('refresh')
        refresh_info = jwt.decode(refresh, settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT_ALGORITHM)

        if refresh_info["user_id"] == request.user.id:
            RefreshToken(refresh).blacklist()

            res = Response({
                "message": "Logout Finished"
            }, status=status.HTTP_200_OK)

            res.delete_cookie('refresh')

            return res

        else:
            return Response({
                "message": "Logout Failed"
            }, status=status.HTTP_401_UNAUTHORIZED)


class QuizView(APIView):
    def get(self, request):
        quizes = Quiz.objects.all()
        serializer = QuizSerializer(quizes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = User.objects.get(id=request.user.id)

        title = request.data["title"]
        quiz_score = request.data["quiz_score"]

        data = {
            "title": title,
            "quiz_score": quiz_score,
            "user": user
        }

        quiz_form = QuizForm(data=data)

        quiz = quiz_form.save()

        if quiz_form.is_valid():

            for value in request.data.get('quiz_question'):
                question = Question()
                question.quiz = quiz
                question.type = value["type"]
                question.content = value["content"]
                question.answer = value["answer"]
                question.save()

            return Response("Quiz Submitted", status=status.HTTP_201_CREATED)
        return Response(quiz_form.errors, status=status.HTTP_400_BAD_REQUEST)




class QuizDetailView(APIView):
    def get_object_or_404(self, quiz_id):
        try:
            return Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise Http404

    def get(self, request, quiz_id):
        quiz = self.get_object_or_404(quiz_id)
        serializer = QuizDetailSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizRankView(APIView):
    def filter_object_or_404(self, quiz_id):
        try:
            return Rank.objects.filter(quiz=quiz_id).order_by('-score')
        except Rank.DoesNotExist:
            raise Http404

    def get(self, request, quiz_id):
        rank = self.filter_object_or_404(quiz_id)
        serializer = RankSerializer(rank, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)