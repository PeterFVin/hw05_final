from django.conf import settings
from django.core.paginator import Paginator


def paginate(request, queryset):
    return {
        'page_obj': Paginator(queryset, settings.NUM_OBJ_ON_PAGE).get_page(
            request.GET.get('page'),
        ),
    }
