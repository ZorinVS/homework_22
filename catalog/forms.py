from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from .utils.mixins import StyleFormMixin
from .utils.validations_utils import check_input, make_warning, convert_size


class ProductForm(StyleFormMixin, forms.ModelForm):
    BANNED_WORDS = [
        "казино", "криптовалюта", "крипта",
        "биржа", "дешево", "бесплатно",
        "обман", "полиция", "радар",
    ]
    FIELDS_WITH_ATTRIBUTES = {
        "name": {"class": "form-control", "placeholder": "Введите название продукта"},
        "description": {"class": "form-control", "placeholder": "Введите описание продукта"},
        "image": {"class": "form-control"},
        "category": {"class": "form-control"},
        "price": {"class": "form-control", "placeholder": "Введите цену товара"},
    }
    VALID_TYPES = ["image/jpeg", "image/png"]  # Допускаются файлы с форматами JPEG или PNG
    IMAGE_SIZE_LIMIT = 5.0  # Допускаются файлы размером до 5 МБ

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        banned_input = check_input(name, self.BANNED_WORDS)  # Поиск запрещенных слов
        if banned_input:
            raise ValidationError(make_warning(banned_input))
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        banned_input = check_input(description, self.BANNED_WORDS)  # Поиск запрещенных слов
        if banned_input:
            raise ValidationError(make_warning(banned_input))
        return description

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            image_format = image.content_type
            if image_format not in self.VALID_TYPES:
                raise ValidationError(f"Формат вашего файла – {image_format.split('/')[1].upper()}! "
                                      f"Допустимые форматы: JPEG и PNG.")

            image_size = convert_size(image.size)
            if image_size > self.IMAGE_SIZE_LIMIT:
                raise ValidationError(f"Размер вашего файла: {image_size} МБ! Изображение не должно превышать "
                                      f"{self.IMAGE_SIZE_LIMIT} МБ.")
        return image

    def clean_price(self):
        price = self.cleaned_data.get("price", -1)
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной!")
        return price
