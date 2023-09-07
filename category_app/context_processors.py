# takes a request as argument and return dictionary of data as context


from category_app.models import Category


def nav_cat_links(request):
    menu_cat = Category.objects.all()
    return dict(menu_cat = menu_cat)