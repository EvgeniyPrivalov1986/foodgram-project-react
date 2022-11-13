from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Ингредиент',
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Еденица измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class TagColor:
    """Модель цвета тэга."""
    BLUE = '#0000FF'
    GREEN = '#008000'
    RED = '#FF0000'
    ORANGE = '#FFCA86'
    WHITE = '#ffffff'
    YELLOW = '#FFFF00'
    COLOR_CHOICES = [
        (BLUE, "Синий"),
        (GREEN, "Зелёный"),
        (RED, "Красный"),
        (ORANGE, "Оранжевый"),
        (WHITE, 'Белый'),
        (YELLOW, "Жёлтый"),
    ]


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Тэг',
        unique=True
    )
    color = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Цвет тэга',
        choices=TagColor.COLOR_CHOICES,
        unique=True
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Группа блюд',
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
