from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Name", help_text="Введите название категории"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Введите описание категории",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Name", help_text="Введите название продукта"
    )
    description = models.TextField(
        verbose_name="Description", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        blank=True, null=True, upload_to="catalog/images/", verbose_name="Image"
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Category",
        help_text="Укажите категорию",
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
        help_text="Укажите цену товара",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["name", "price", "updated_at"]


class Contact(models.Model):
    country = models.CharField(
        max_length=60, verbose_name="County", help_text="Введите название страны"
    )
    tin = models.CharField(
        max_length=20, verbose_name="Tax Identification Number", help_text="Введите ИНН"
    )
    address = models.TextField(verbose_name="Address", help_text="Введите адрес")

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"
