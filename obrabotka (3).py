def clean_phone_number(summa_do_obr):
    try:
        # Удаление всех символов, кроме чисел и запятых
        result = "".join(char for char in summa_do_obr if char.isnumeric() or char == ",")
        return result
    except Exception:
        # Возвращаем исходное значение при любой ошибке
        return summa_do_obr
