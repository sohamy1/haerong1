from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager): # 잘 이해해보려고 노력하기

    def create_user(self, email, nickname, password):

        user = self.model(
            email = email,
            nickname = nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):

        user = self.create_user(email, nickname, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    nickname = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to = "profile/", default='profile/basic_profile.gif')
    score = models.IntegerField(default=0)
    rank = models.CharField(max_length=10, default="브론즈")
    question_key = models.CharField(max_length=100)
    question_value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'user'