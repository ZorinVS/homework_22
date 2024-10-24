from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.management import call_command
from tabulate import tabulate
from .models import Contact, Product


def home(request):
    """Контроллер для отображения главной страницы"""

    # Проверка наличия продуктов в БД
    has_products = Product.objects.exists()
    if not has_products:
        # Загрузка данный из фикстур
        call_command("loaddata", "categories_fixture.json")
        call_command("loaddata", "products_fixture.json")
        call_command("loaddata", "contact_fixture.json")

    # Выборка последних 5 продуктов по дате создания
    last_five_products = Product.objects.order_by("-created_at")[:5]

    # Подготовка данных к выводу в консоль
    products_data = [
        (product.name, product.created_at) for product in last_five_products
    ]
    table_headers = ("Продукт", "Дата создания")
    # Печать данных в консоль в виде таблицы
    print(tabulate(products_data, headers=table_headers, tablefmt="fancy_grid"))

    return render(
        request,
        template_name="catalog/home.html",
        context={"products": last_five_products},
    )


def contacts(request):
    """Контроллер для отображения страницы с контактной информацией"""

    if request.method == "POST":
        name = request.POST.get("name")
        # phone = request.POST.get("phone")
        # message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")

    # Отображение контактной информации последнего добавления
    latest_contact_info = Contact.objects.order_by("-id")[0]

    return render(
        request,
        template_name="catalog/contacts.html",
        context={"contact_info": latest_contact_info},
    )


def category_products(request, category_name):
    """Контроллер для отображения списка продуктов конкретной категории"""

    # Словарь содержащий человеко-читаемые названия категорий
    categories_dict = {
        "mailing-lists": "Рассылки",
        "telegram-bots": "Телеграм боты",
        "useful-utilities": "Полезные утилиты",
        "web-applications": "Веб-приложения",
        "microservices": "Микросервисы",
    }
    # Получение названия категории
    category_name = categories_dict.get(category_name)
    if not category_name:
        raise Http404("Category not found")

    # Фильтрация продуктов по полученному названию категории
    the_products = Product.objects.filter(category__name=category_name)

    context = {
        "category_name": category_name,
        "products": the_products,
    }

    return render(
        request,
        template_name="catalog/category_products.html",
        context=context,
    )


def product_detail(request, pk):
    """Контроллер для отображения страницы с подробной информацией о товаре"""

    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product,
        "product_id": pk,
    }

    return render(request, "catalog/product_detail.html", context=context)
