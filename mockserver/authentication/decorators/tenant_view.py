from django.http import Http404


def tenancy_required(fn):
    def wrap(request, *args, **kwargs):
        if request.tenant is None:
            raise Http404
        return fn(request, *args, **kwargs)

    return wrap
