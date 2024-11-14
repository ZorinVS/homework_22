def check_input(field_data: str, banned_words: list) -> str | list:
    """ Проверка входных данных на наличие запрещенных слов """

    # Перевод слов в нижний регистр
    field_data_lower = [word.lower() for word in field_data.split()]
    banned_words_lower = [word.lower() for word in banned_words]

    # Список для хранения найденных запрещенных слов
    dangers_found = []

    for danger in banned_words_lower:
        if len(field_data_lower) == 1 and danger in field_data_lower:
            return danger
        elif danger in field_data_lower:
            dangers_found.append(danger)

    is_one = len(dangers_found) == 1
    return dangers_found[0] if is_one else dangers_found


def make_warning(banned_input: str | list) -> str:
    """ Создание сообщения-предупреждения о наличии запрещенных слов """

    if isinstance(banned_input, str):
        return f"Обнаружено запрещенное слово {banned_input.upper()}! Спам не допускается!"
    else:
        return f"Обнаружены запрещенные слова: {', '.join(banned_input)}! Спам не допускается!"


def convert_size(size: int | float, unit: str = "b") -> int | float:
    """
    Преобразует размер файла между байтами и мегабайтами.

    По умолчанию функция конвертирует байты в мегабайты, если в качестве единицы измерения
    указаны байты ("b"), и наоборот, если указаны мегабайты ("mb").
    """
    size_ratio = 1024 ** 2
    return round(size * size_ratio, 1) if unit == "mb" else round(size / size_ratio, 1)


if __name__ == "__main__":
    s = float(input("Размер: "))
    u = input("Единица: ")

    if u:
        res = convert_size(s, u)
    else:
        res = convert_size(s)

    print(res)
