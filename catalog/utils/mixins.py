class StyleFormMixin:
    """ Mixin для стилизации формы """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ""  # Исключение отображения help_text в форме
            try:
                attributes = self.FIELDS_WITH_ATTRIBUTES.get(field_name)
            except AttributeError:
                field.widget.attrs["class"] = "form-control"
            else:
                if attributes:
                    field.widget.attrs.update(attributes)
