from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка админ панели модели тегов."""
    list_display = (
        'name',
        'color',
        'slug'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка админ панели модели ингредиентов."""
    list_display = (
        'name',
        'measurement_unit'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка админ панели модели рецептов."""
    list_display = (
        'name',
        'author',
        'tags',
        'in_favorite'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('in_favorite',)
    filter_horizontal = ('tags',)
    inlines = (IngredientRecipeInline,)

    def in_favorite(self, obj):
        """Считает количество добавлений в избранное."""
        return obj.in_favorite.all().count()

    in_favorite.short_description = 'Количество добавлений в избранное'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Настройка админ панели модели ингредиентов в рецепте."""
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('recipe', 'ingredient')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Настройка админ панели модели избранных рецептов."""
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Настройка админ панели модели продуктовой корзины."""
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user',)
