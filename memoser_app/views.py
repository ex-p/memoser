import json

from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello')


def request_token(request):
    if request.method == 'POST':
        data = {
            'error': None
        }

        # body = json.loads(request.body)
        # content = body['content']
        # print(content)
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse('404')

