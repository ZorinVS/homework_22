from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Contact, Product


class HomeListView(ListView):
    model = Product
    template_name = "catalog/home.html"

    def get_queryset(self):
        # return Product.objects.order_by("-created_at")[:5]
        return Product.objects.filter(is_published=True)


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        contacts = Contact.objects.order_by("-id")
        context_data["contact_info"] = contacts[0] if contacts.exists() else None
        return context_data

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Имеется новое сообщение от {name} {phone}: {message}")
        context_data = self.get_context_data()
        context_data["message"] = f"Спасибо, {name}! Сообщение получено :)"
        return self.render_to_response(context_data)


class CategoryProductsListView(ListView):
    model = Product
    template_name = "catalog/category_products.html"

    # Словарь содержащий человеко-читаемые названия категорий
    categories_dict = {
        "mailing-lists": "Рассылки",
        "telegram-bots": "Телеграм боты",
        "useful-utilities": "Полезные утилиты",
        "web-applications": "Веб-приложения",
        "microservices": "Микросервисы",
    }

    def get_queryset(self):
        category_key = self.kwargs.get("category_name")
        self.category_name = self.categories_dict.get(category_key)
        if not self.category_name:
            raise Http404("Category not found")
        return Product.objects.filter(category__name=self.category_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_name"] = self.category_name
        return context


class UnpublishedProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/products_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(is_published=False)
        # Просмотр всех неопубликованных продуктов доступен только для модератора
        if not user.has_perm("catalog.can_unpublish_product"):
            queryset = queryset.filter(owner=user)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Неопубликованное"
        context_data["header"] = "Неопубликованные продукты"
        return context_data


class UserProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/products_list.html"

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Продукты пользователя"
        context_data["header"] = "Мои продукты"
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = self.request.user
        product = form.instance
        # Если пользователь является модератором
        if user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied
        product.owner = user
        if self.request.POST.get("action") == "publish":
            form.instance.is_published = True
        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_object(self):
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        user = self.request.user
        if user != product.owner and not user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied
        return product

    def post(self, request, pk):
        product = self.get_object()
        if request.POST.get("action") == "unpublish":
            if not self.request.user.has_perm("catalog.can_unpublish_product"):
                raise PermissionDenied
            product.is_published = False
            product.save()
        return redirect("catalog:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = self.request.user
        product = get_object_or_404(Product, pk=self.kwargs["pk"])

        if user != product.owner:
            raise PermissionDenied

        if self.request.POST.get("action") == "publish":
            form.instance.is_published = True
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = self.request.user
        product = self.get_object()
        if user != product.owner and not user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied
        return super().form_valid(form)
