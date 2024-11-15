from django import forms
from .models import Article
from catalog.utils.mixins import StyleFormMixin


class ArticleForm(StyleFormMixin, forms.ModelForm):
    FIELDS_WITH_ATTRIBUTES = {
        "title": {"class": "form-control", "placeholder": "Введите заголовок статьи"},
        "body": {"class": "form-control", "placeholder": "Введите содержимое статьи"},
        "preview": {"class": "form-control"},
    }

    class Meta:
        model = Article
        fields = ["title", "body", "preview"]
