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


class Follow(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            ),
        )

    def __str__(self):
        return self.user
