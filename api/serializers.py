from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


User = get_user_model()


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = [
            'nickname',
            'score',
            'created_at'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'type',
            'content',
            'answer',
        ]


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = [
            'id',
            'user',
            'title',
            'quiz_score',
        ]


class QuizDetailSerializer(serializers.ModelSerializer):

    quiz_question = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'quiz_score',
            'quiz_question',
        ]


class UserSerializer(serializers.ModelSerializer):

    user_quiz = QuizSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'user_quiz',
        ]


# 회원가입
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            nickname=validated_data['nickname'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user