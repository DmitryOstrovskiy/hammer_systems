from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string

from django.conf import settings


def generate_invite_code():
    return ''.join([random.choice(list(string.ascii_uppercase + string.digits))
                    for x in range(6)])


class InviteCode(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='владелец кода'
    )
    invite_code = models.CharField(
        max_length=6,
        default=generate_invite_code,
        verbose_name='код приглашения'
    )


class User(AbstractUser):
    username = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        verbose_name='Псевдоним'
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия'
    )
    telephone_number = models.CharField(
        max_length=11,
        blank=True,
        unique=True,
        verbose_name='номер телефона'
    )
    invite_code = models.CharField(
        max_length=11,
        blank=True,
        verbose_name='пригласительный код'
    )
    invite_code_incerd = models.CharField(
        max_length=11,
        blank=True,
        verbose_name='введенный пригласительный код'
    )
    invite_code_list = models.ManyToManyField(
        InviteCode,
        through='InviteCodeincerted'
    )

    USERNAME_FIELD = 'telephone_number'
    REQUIRED_FIELDS = ('username',)


class InviteCodeincerted(models.Model):
    invite_code = models.ForeignKey(InviteCode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


def generate_activation_code():
    return ''.join([random.choice(list('123456789')) for x in range(4)])


class ActivationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    code = models.CharField(max_length=4, default=generate_activation_code)
