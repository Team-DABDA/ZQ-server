from django import forms
from .models import *


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'