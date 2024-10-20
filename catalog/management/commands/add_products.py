from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test products from fixture files to the database"

    def handle(self, *args, **options):
        # Удаление данных перед загрузкой
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузка данный из фикстур
        call_command("loaddata", "categories_fixture.json")
        call_command("loaddata", "products_fixture.json")
        self.stdout.write(
            self.style.SUCCESS("Successfully loaded data from fixture files")
        )

        # category, _ = Category.objects.get_or_create(
        #     name="Рассылки", description="Сервисы и инструменты для создания и автоматизации email и SMS рассылок"
        # )
        #
        # products_data = [
        #     {
        #         "name": "Удобный сервис рассылок",
        #         "description": "- Неограниченная лицензия\n- Поддержка\n- Установка на сервер",
        #         "category": category,
        #         "price": "140.00",
        #     },
        #     {
        #         "name": "SMS уведомления",
        #         "description": "Сервис для мгновенной отправки SMS уведомлений",
        #         "category": category,
        #         "price": "90.00",
        #     },
        # ]
        #
        # for product_data in products_data:
        #     product, created = Product.objects.get_or_create(**product_data)
        #     if created:
        #         self.stdout.write(self.style.SUCCESS(f"Successfully added product: {product.name}"))
        #     else:
        #         self.stdout.write(self.style.WARNING(f"Product already exists: {product.name}"))
