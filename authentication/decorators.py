from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


# Redirect authenticated users to a different URL.
def redirect_authenticated_user(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('index'))
        return view_func(request, *args, **kwargs)
    return wrapped_view