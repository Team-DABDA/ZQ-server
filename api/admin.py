from django.contrib import admin
from .models import *

class QuestionInline(admin.TabularInline):
    model = Question

class QuizAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)


admin.site.register(User)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Rank)