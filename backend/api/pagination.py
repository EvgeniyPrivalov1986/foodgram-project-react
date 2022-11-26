from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинация рецептов на главной странице."""
    page_size_query_param = 'limit'
    page_size = settings.COUNT_RECIPES_IN_PAGE
