from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Управление пользователями через админ панель."""
    list_display = (
        'id',
        'role',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_display_links = ('id', 'username')
    search_fields = ('role', 'username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Управление подписками через админ панель."""
    list_display = (
        'id',
        'user',
        'author'
    )
    list_display_links = ('id', 'user')
    search_fields = ('user',)
