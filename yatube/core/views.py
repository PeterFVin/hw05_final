from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    del exception
    return render(
        request,
        'core/404.html',
        {'path': request.path},
        status=HTTPStatus.NOT_FOUND,
    )


def csrf_failure(request, reason=''):
    del reason
    return render(request, 'core/403csrf.html')
