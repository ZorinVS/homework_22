from catalog import views
from catalog.apps import CatalogConfig
from django.urls import path

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("contacts/", views.ContactsTemplateView.as_view(), name="contacts"),
    path(
        "category-<str:category_name>/",
        views.CategoryProductsListView.as_view(),
        name="category_products",
    ),
    path("product-detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
]
