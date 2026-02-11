from django.conf import settings


def uwtheme(request):
    return {
        'CLUSTER_WEB_HOST': settings.MAILMAN_CLUSTER_WEB_HOST
    }
