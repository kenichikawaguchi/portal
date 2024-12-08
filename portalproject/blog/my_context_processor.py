from django.conf import settings


def common(request):
    return {"site_title": settings.TITLE,
            "favicon": settings.FAVICON,
            "site_subtitle": settings.SUBTITLE,
            "facebook": settings.FACEBOOK,
           }

