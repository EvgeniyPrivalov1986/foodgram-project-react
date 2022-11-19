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


class Recipe(models.Model):
    """Модель рецептов."""    
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        verbose_name='Список ингредиентов',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Название рецепта',
        unique=True
    )
    text = models.TextField(
        verbose_name='Рецепт блюда',
        unique=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                settings.MIN_COOKING_TIME, 
                settings.MIN_COOKING_TIME_ERROR
            ),
            MaxValueValidator(
                settings.MAX_COOKING_TIME, 
                settings.MAX_COOKING_TIME_ERROR
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    """Модель списка ингредиентов.""" 
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                settings.MIN_AMOUNT_INGREDIENT, 
                settings.MIN_AMOUNT_INGREDIENT_ERROR, 
            )
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe'
            )
        ]


class Favourite(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    """Модель продуктовой корзины."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_shopping_list'
            )
        ]

    def __str__(self):
        return self.user
