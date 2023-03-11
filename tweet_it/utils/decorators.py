from functools import wraps

from django.http import HttpResponseBadRequest


def ajax_required(f):
    @wraps
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    return wrap
