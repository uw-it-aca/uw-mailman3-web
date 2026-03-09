from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode
import logging


logger = logging.getLogger(__name__)


class AuthenticationRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.GET.get('is_authenticated', '') == 'true':
                # remove is_authenticated from parameters
                params = request.GET.copy()
                del params['is_authenticated']
                query_string = f"?{urlencode(params)}" if params else ""

                login_url = f"/saml/login?next={request.path}{query_string}"
                return redirect(login_url)
        except Exception as ex:
            logger.error(f"Cannot get revers paths: {ex}")

        return self.get_response(request)
