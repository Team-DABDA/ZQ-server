from rest_framework import serializers
from .models import *


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = [
            'id',
            'quiz',
            'nickname',
            'score',
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = [
            'id',
            'quiz',
            'type',
            'content',
            'answer',
        ]


class QuizSerializer(serializers.ModelSerializer):

    quiz_question = QuestionSerializer(many=True)
    quiz_rank = RankSerializer(many=True)

    class Meta:
        model = Rank
        fields = [
            'id',
            'user',
            'title',
            'quiz_score',
            'quiz_question',
            'quiz_rank',
        ]


class UserSerializer(serializers.ModelSerializer):

    user_quiz = QuizSerializer(many=True)

    class Meta:
        model = Rank
        fields = [
            'id',
            'nickname',
            'user_quiz',
        ]