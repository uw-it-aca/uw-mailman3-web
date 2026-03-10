from django.conf import settings


def uwtheme(request):
    session_index = request.session.get('samlSessionIndex')
    return {
        'CLUSTER_WEB_HOST': settings.MAILMAN_CLUSTER_WEB_HOST,
        'IS_SAML_AUTHENTICATED': session_index is not None
    }
