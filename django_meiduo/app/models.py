from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """⾃定义⽤户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='⼿机号')
    # USERNAME_FIELD = 'mobile'
    nick_name = models.CharField(max_length=20, default="未知⽤户")
    class Meta:
        db_table = 'tb_users'
        verbose_name = '⽤户管理'
        verbose_name_plural = verbose_name


def __str__(self):
    return self.username
