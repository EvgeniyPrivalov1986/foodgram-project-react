from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import IngredientSearchFilter, RecipeFilterSet
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CartSerializer, CreateRecipeSerializer,
                          FavoriteSerializer, FollowListSerializer,
                          FollowSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)
from .utils import download_shopping_cart_response
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Follow, User


class UsersViewSet(UserViewSet):
    """Viewset для пользователей и подписок."""
    pagination_class = CustomPagination

    @action(['get'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        """Получает текущего пользователя."""
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        """Получает список авторов, на которых подписан пользователь."""
        subscriptions_list = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = FollowListSerializer(
            subscriptions_list, many=True, context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        """Текущий пользователь подписывается/отписывается от автора."""
        if request.method != 'POST':
            subscription = get_object_or_404(
                Follow,
                author=get_object_or_404(User, id=id),
                user=request.user
            )
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FollowSerializer(
            data={
                'user': request.user.id,
                'author': get_object_or_404(User, id=id).id
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecipeViewSet(ModelViewSet):
    """Viewset для рецептов, продуктовой корзины и избранного."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    permission_classes = (IsAuthorOrAdminOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_serializer_class(self):
        """Проверяет тип запроса и определяет класс сериализатора."""
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return CreateRecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        """Действия для POST-запросов."""
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        """Действия для DELETE-запросов."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_instance = get_object_or_404(model, user=user, recipe=recipe)
        model_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk):
        """Добавляет рецепт в продуктовую корзину."""
        return self.post_method_for_actions(
            request, pk, serializers=CartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаляет рецепт из продуктовой корзины."""
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Cart
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Запрашивает загрузку списка ингредиентов из продуктовой корзины."""
        shopping_list = IngredientRecipe.objects.filter(
            recipe__cart__user=request.user
        ).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')
        ).annotate(amount=Sum('amount')).values_list(
            'ingredient__name',
            'amount',
            'ingredient__measurement_unit'
        )        
        return download_shopping_cart_response(shopping_list)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        """Добавляет рецепт в избранное."""
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаляет рецепт из избранного."""
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)


class IngredientViewSet(ModelViewSet):
    """Viewset для игредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(ModelViewSet):
    """Viewset для тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
