from django.conf import settings
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Follow, User


class UsersSerializer(UserSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj: User):
        """Проверяет, подписан ли пользователь на автора рецепта."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj).exists()


class FollowSerializer(ModelSerializer):
    """Сериализатор для подписок."""
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        """Проверяет подписки."""
        get_object_or_404(User, username=data['author'])
        if self.context['request'].user == data['author']:
            raise ValidationError({
                'errors': settings.USER_FOLLOWING_HIMSELF_ERROR
            })
        if Follow.objects.filter(
                user=self.context['request'].user,
                author=data['author']
        ):
            raise ValidationError({
                'errors': settings.USER_FOLLOWING_FOLLOWER_ERROR
            })
        return data

    def to_representation(self, instance):
        """Отображает подписки."""
        return FollowListSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data


class FollowListSerializer(ModelSerializer):
    """Сериализатор для списка авторов, на которых подписан пользователь."""
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, author):
        """Получает количество рецептов автора."""
        return Recipe.objects.filter(author=author).count()

    def get_recipes(self, author):
        """Получает рецепты автора."""
        queryset = self.context.get('request')
        recipes_limit = queryset.query_params.get('recipes_limit')
        if not recipes_limit:
            return RecipeShortInfo(
                Recipe.objects.filter(author=author),
                many=True, context={'request': queryset}
            ).data
        return RecipeShortInfo(
            Recipe.objects.filter(author=author)[:int(recipes_limit)],
            many=True,
            context={'request': queryset}
        ).data

    def get_is_subscribed(self, author):
        """Проверяет подписан ли пользователь на автора."""
        return Follow.objects.filter(
            user=self.context.get('request').user,
            author=author
        ).exists()


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientRecipeSerializer(ModelSerializer):
    """Сериализатор для игредиентов в рецепте."""
    id = PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    measurement_unit = SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True,
    )
    name = SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='ingridients_recipe',
    )
    author = UsersSerializer(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    is_favorited = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Проверяет добавлен ли рецепт в избранное."""
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe__id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверяет добавлен ли рецепт в продуктовую корзину."""
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=request.user, recipe__id=obj.id).exists()


class CreateIngredientRecipeSerializer(ModelSerializer):
    """Сериализатор для создания ингредиента."""
    id = PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )

    def validate_amount(self, data):
        """Проверяет количество игредиентов в рецепте."""
        if int(data) < settings.MIN_AMOUNT_INGREDIENT:
            raise ValidationError({
                'ingredients': settings.MIN_AMOUNT_INGREDIENT_ERROR
            })
        return data

    def create(self, validated_data):
        """Создает игредиент."""
        return IngredientRecipe.objects.create(
            ingredient=validated_data.get('id'),
            amount=validated_data.get('amount')
        )


class CreateRecipeSerializer(ModelSerializer):
    """Сериализатор для создания рецепта."""
    image = Base64ImageField(use_url=True, max_length=None)
    author = UsersSerializer(read_only=True)
    ingredients = CreateIngredientRecipeSerializer(many=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    cooking_time = IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'image', 'tags', 'author', 'ingredients',
            'name', 'text', 'cooking_time',
        )

    def create_ingredients(self, recipe, ingredients):
        """Создает игредиенты."""
        IngredientRecipe.objects.bulk_create([
            IngredientRecipe(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['ingredient'],
            ) for ingredient in ingredients
        ])

    def validate(self, data):
        """Проверяет игредиенты в рецепте и время приготовления."""
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise ValidationError(
                    settings.ADD_INGREDIENTS_IN_RECIPES_ERROR
                )
            ingredients_list.append(ingredient_id)
        if data['cooking_time'] <= settings.MIN_COOKING_TIME:
            raise ValidationError(
                settings.MIN_COOKING_TIME_ERROR
            )
        return data

    @atomic
    def create(self, validated_data):
        """Создает рецепт."""
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Редактирует рецепт."""
        ingredients = validated_data.pop('ingredients')
        recipe = instance
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        self.create_ingredients(recipe, ingredients)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        """Отображает созданный/отредактированный рецепт."""
        return RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request'),
            }
        ).data


class RecipeShortInfo(ModelSerializer):
    """Сериализатор для страницы рецепта."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CartSerializer(ModelSerializer):
    """Сериализатор для продуктовой корзины."""
    class Meta:
        fields = ['recipe', 'user']
        model = Cart

    def validate(self, data):
        """Проверяет наличие рецепта в корзине."""
        request = self.context.get('request')
        recipe = data['recipe']
        if Cart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            raise ValidationError({
                'errors': settings.ADD_RECIPES_IN_SHOPPING_CART_ERROR
            })
        return data

    def to_representation(self, instance):
        """Отображает продуктовую корзину."""
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortInfo(instance.recipe, context=context).data


class FavoriteSerializer(ModelSerializer):
    """Сериализатор для избранных рецептов."""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        """Проверяет наличие рецепта в избранном."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            raise ValidationError({
                'errors': settings.ADD_RECIPES_IN_FAVORITE_ERROR
            })
        return data

    def to_representation(self, instance):
        """Отображает избранные рецепты."""
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortInfo(
            instance.recipe, context=context).data
