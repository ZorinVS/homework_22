from django.http import HttpResponse
from django.shortcuts import render
from django.core.management import call_command
from tabulate import tabulate
from .models import Product, Contact


def home(request):
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
        context={"latest_products": last_five_products},
    )


def contacts(request):
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
