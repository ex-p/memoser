import json
import logging

from django.http import HttpResponse
from django.views import View

from memoser_app.logic import verify_openapi_auth

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def index(request):
    return HttpResponse('')


class RequestTokenView(View):
    def post(self, request, *args, **kwargs):
        body = request.body
        response = {'error': None, 'request': body}
        if not body:
            response['error'] = 'No data provided'
        else:
            try:
                response['verified'] = verify_openapi_auth(body)
            except Exception as e:
                response['error'] = str(e)
        return HttpResponse(json.dumps(response), content_type='application/json')
