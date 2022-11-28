from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def download_shopping_cart_response(shopping_list):
    """
    Скачивает список ингредиентов из продуктовой корзины в формате .txt.
    Пользователь получает файл с необходимыми ингредиентами для всех
    добавленных в продуктовую корзину рецептов.
    """
    html_template = render_to_string(
        'recipes/pdf_template.html',
        {'ingredients': shopping_list}
    )
    html = HTML(string=html_template)
    result = html.write_pdf()
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=shopping_list.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    return response
