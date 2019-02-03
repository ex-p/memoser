import json

from django.http import HttpResponse
from django.views import View

from memoser_app.logic import verify_openapi_auth


def index(request):
    return HttpResponse('Hello')


def request_token(request):
    if request.method == 'POST':
        data = {
            'error': None
        }

        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse('404')


class RequestTokenView(View):
    def post(self, request, *args, **kwargs):
        response = {'error': None}
        body = request.body
        if not body:
            response['error'] = 'No data provided'
        else:
            try:
                response['verified'] = verify_openapi_auth(body)
            except Exception as e:
                response['error'] = str(e)
        return HttpResponse(json.dumps(response), content_type='application/json')
