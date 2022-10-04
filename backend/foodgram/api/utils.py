from django.http import HttpResponse


def get_cart_txt(ingredients):
    """Function to generate txt file for shopping list."""
    content_list = []
    for ingredient in ingredients:
        content_list.append(
            f'{ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]}): '
            f'{ingredient["total_amount"]}')
    content = 'Ваш список покупок:\n\n' + '\n'.join(content_list)
    filename = 'shopping_cart.txt'
    file = HttpResponse(content, content_type='text/plain')
    file['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return file
