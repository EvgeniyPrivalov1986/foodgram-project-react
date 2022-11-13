from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    """Модель роли пользователей."""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    ]


class User(AbstractUser):
    """Модель пользователей."""
    username = models.CharField(
        unique=True,
        max_length=settings.MAX_LENGTH,
        blank=False,
        verbose_name='username'
    )
    email = models.EmailField(
        'Почта пользователя',
        max_length=settings.MAX_LENGTH,
        unique=True
    )
    first_name = models.TextField(
        max_length=settings.MAX_LENGTH,
        unique=True
    )
    last_name = models.TextField(
        max_length=settings.MAX_LENGTH,
        unique=True
    )
    role = models.CharField(
        choices=UserRole.ROLES,
        default=UserRole.USER,
        max_length=settings.MAX_LENGTH,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
