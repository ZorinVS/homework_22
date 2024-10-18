from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, template_name="catalog/home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        # phone = request.POST.get("phone")
        # phone = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
    return render(request, template_name="catalog/contacts.html")
