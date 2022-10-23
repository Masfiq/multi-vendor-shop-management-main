from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import redirect,  get_object_or_404

from .models import Investor


def staff_only(view_func):
        def wrapper_function(request, *args, **kwargs):
                if request.user.is_staff:
                    return view_func(request, *args, **kwargs)
                else:
                    investor = get_object_or_404(Investor, user=request.user)
                    if investor:
                        return redirect('investor_dashboard')
                    else:
                        raise Http404("I don't understand you!")
            
        return wrapper_function



def admin_only(view_func):
        def wrapper_function(request, *args, **kwargs):
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            
        return wrapper_function