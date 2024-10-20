from django.conf import settings


def common(request):
    return {"site_title": settings.TITLE}

