from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog import services
from catalog.forms import ProductForm
from catalog.models import Product


class HomeListView(ListView):
    model = Product
    template_name = "catalog/home.html"

    def get_queryset(self):
        # return Product.objects.order_by("-created_at")[:5]
        return services.get_products_list_from_cache("publication", True, "published_products")


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return services.get_contact_info(context_data)

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
    category_name = None

    def get_queryset(self):
        category_key = self.kwargs.get("category_name")
        self.category_name, queryset = services.get_products_by_category(category_key)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return services.set_context_data(context=context_data, category_name=self.category_name)


class UnpublishedProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/products_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = services.get_products_list_from_cache("publication", False, "unpublished_products")
        return services.get_unpublished_products(queryset, user)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return services.set_context_data(context_data, title="Неопубликованное", header="Неопубликованные продукты")


class UserProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/products_list.html"

    def get_queryset(self):
        user = self.request.user
        return services.get_products_list_from_cache(filter_by="owner", value=user)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return services.set_context_data(context_data, title="Продукты пользователя", header="Мои продукты")


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = self.request.user
        product = form.instance
        # Если пользователь является модератором
        if user.has_perm("catalog.can_unpublish_product") and not user.is_superuser:
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
