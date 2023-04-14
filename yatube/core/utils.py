from django.conf import settings
from django.core.paginator import Paginator


def paginate(request, queryset):
    return {
        'paginator': Paginator(queryset, settings.NUM_POSTS_ON_PAGE),
        'page_number': request.GET.get('page'),
        'page_obj': Paginator(queryset, settings.NUM_POSTS_ON_PAGE).get_page(
            request.GET.get('page'),
        ),
    }
