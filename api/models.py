from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, nickname, password=None):
        if not nickname:
            raise ValueError('User must have nickname')
        user = self.model(
            nickname=nickname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password):
        user = self.create_user(
            nickname=nickname,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    nickname = models.CharField(max_length=20, unique=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'nickname'

    def __str__(self):
        return '[{}] {}'.format(self.id, self.nickname)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Quiz(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_quiz')

    title = models.CharField(max_length=50)
    quiz_score = models.IntegerField()

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)


class Question(BaseModel):

    TYPE_CHOICE = [
        ('t-f', '참/거짓'),
        ('short-answer', '주관식')
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_question')

    type = models.CharField(max_length=50, choices=TYPE_CHOICE, default='t-f')
    content = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return '[QUIZ#{} : {}] {} ({})'.format(self.quiz, self.id, self.content, self.type)


class Rank(BaseModel):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_rank')

    nickname = models.CharField(max_length=20)
    score = models.IntegerField()

    def __str__(self):
        return '[QUIZ#{} : {}] {}'.format(self.quiz, self.nickname, self.score)