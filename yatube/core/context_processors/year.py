import datetime as dt
from typing import Dict

from django.http import HttpRequest


def year(request: HttpRequest) -> Dict[str, int]:
    """Добавляет переменную с текущим годом.

    Args:
        request: Неиспользуемая переменная, удаляется.

    Returns:
        Функция возвращает текущий год, используется в footer.

    """
    del request
    return {
        'year': dt.datetime.today().year,
    }
