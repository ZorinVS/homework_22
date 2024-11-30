from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.core.management import call_command


from catalog.models import Product
from users.models import User

USERS_DATA = (
    {
        "email": "sebastian@gmx.com",
        "avatar": "users/avatars/Sebastian.png",
        "country": "USA",
        "password": "moderator",
    },
    {
        "email": "colt@gmx.com",
        "avatar": "users/avatars/ColtSeavers.png",
        "country": "USA",
        "password": "user_colt",
    },
    {
        "email": "ken@gmx.com",
        "avatar": "users/avatars/Ken.png",
        "country": "USA",
        "password": "user_ken",
    },
    {
        "email": "holland@gmx.com",
        "avatar": "users/avatars/HollandMarch.png",
        "country": "USA",
        "password": "user_holland",
     },
)


class Command(BaseCommand):
    help = "Команда для инициализации проекта тестовыми данными"

    def handle(self, *args, **options):
        self.stdout.write("Инициализируем проект...")

        # Создание группы 'Модератор продуктов'
        moderators_group = Group.objects.create(name="Модератор продуктов")

        # Предоставление права 'delete_product'
        delete_permission = Permission.objects.get(codename="delete_product")
        moderators_group.permissions.add(delete_permission)

        # Предоставление кастомного права 'can_unpublish_product'
        content_type = ContentType.objects.get_for_model(Product)
        unpublish_permission = Permission.objects.get(
            codename="can_unpublish_product",
            content_type=content_type,
        )
        moderators_group.permissions.add(unpublish_permission)

        # Сохранение группы
        moderators_group.save()
        self.stdout.write(self.style.SUCCESS("25% – Создана группа 'Модератор продуктов'"))

        # Создание пользователей
        for user_data in USERS_DATA:
            user = User.objects.create(
                email=user_data["email"],
                avatar=user_data["avatar"],
                country=user_data["country"],
            )
            user.set_password(user_data["password"])

            # Предоставление прав модератора пользователю 'sebastian@gmx.com'
            if user.email == "sebastian@gmx.com":
                user.groups.add(moderators_group)

            user.save()
        self.stdout.write(self.style.SUCCESS("50% – Созданы пользователи и назначен модератор"))

        # Загрузка категорий продуктов
        call_command("loaddata", "categories_fixture.json")

        # Загрузка продуктов
        call_command("loaddata", "products_fixture.json")
        self.stdout.write(self.style.SUCCESS("75% – Добавлены категории и продукты пользователей"))

        # Загрузка данных для страницы 'Контакты'
        call_command("loaddata", "contact_fixture.json")
        self.stdout.write(self.style.SUCCESS("100% – Добавлена контактная информация"))

        self.stdout.write(self.style.SUCCESS("Проект успешно инициализирован"))
