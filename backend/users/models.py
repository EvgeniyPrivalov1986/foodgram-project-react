from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    USER = 'user'
    ADMIN = 'admin'
    choices = [
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    ]


class User(AbstractUser):
    """Модель пользователей."""
    username = models.CharField(
        max_length=settings.MAX_LENGTH,
        unique=True,
        verbose_name='Username'
    )
    email = models.EmailField(
        'Электронная почта',
        help_text='Электронная почта пользователя',
        max_length=settings.MAX_LENGTH,
        unique=True
    )
    first_name = models.TextField(
        'Имя пользователя',
        help_text='Имя пользователя',
        max_length=settings.MAX_LENGTH,
    )
    last_name = models.TextField(
        'Фамилия пользователя',
        help_text='Фамилия пользователя',
        max_length=settings.MAX_LENGTH,
    )
    role = models.TextField(
        'Роль',
        help_text='Роль пользователя',
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('id',)
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
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription_user_author'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}.'
