from django.shortcuts import render


def welcome_page(request):
    """Render the public landing page."""
    return render(request, "core/index.html")


def ptsd_info(request):
    """Render informational page about PTSD."""
    return render(request, "core/ptsdinfo.html")


def books(request):
    """Render page with downloadable book recommendations."""
    return render(request, "core/downloadbooks.html")


def selfhelp(request):
    """Render self-help techniques page."""
    return render(request, "core/selfhelp.html")