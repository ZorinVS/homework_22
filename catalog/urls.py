from catalog import views
from catalog.apps import CatalogConfig
from django.urls import path

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path(
        "category-<str:category_name>/",
        views.category_products,
        name="category_products",
    ),
    path("product-detail/<int:pk>/", views.product_detail, name="product_detail"),
]
