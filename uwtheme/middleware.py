from django.shortcuts import redirect
from urllib.parse import urlencode
import logging


logger = logging.getLogger(__name__)


class AuthenticationRedirectMiddleware:
    """  Redirect through saml login if request is not authenticated, but
         request contains a cue that authentication should be attempted
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.GET.get('is_authenticated', '') == 'true':
            # snip is_authenticated from query params to avoid confusion
            params = request.GET.copy()
            del params['is_authenticated']
            request.GET = params

            if not request.user.is_authenticated:
                query_string = f"?{urlencode(params)}" if params else ""
                login_url = f"/saml/login?next={request.path}{query_string}"

                logger.debug(f"Auth Redirect: redirecting to {login_url}")

                return redirect(login_url)

        return self.get_response(request)
