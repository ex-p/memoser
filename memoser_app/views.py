import json
import logging
from abc import ABC

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from memoser_app.logic import verify_openapi_auth

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def index(request):
    return HttpResponse('')


class RequestTokenView(View):
    def post(self, request, *args, **kwargs):
        body = request.body.decode('utf-8')
        response = {'error': None, 'request': body}

        try:
            if not body:
                raise Exception('No data provided')

            data = json.loads(body)
            verified, mid = verify_openapi_auth(data['cookies'])
            if not verified:
                raise Exception('Not verified')
            name = 'vk{}'.format(mid)
            user = User.objects.filter(username=name)
            if not user.exists():
                first_name = data['user']['name']
                image = data['user']['image']
                User.objects.create_user(username=user, first_name=first_name, last_name=image)
                user = User.objects.filter(username=name)
            user = user.first()
            response['access_token'] = ExtendedTokenObtainPairSerializer.get_token(user)
        except Exception as e:
            response['error'] = str(e)
        return HttpResponse(json.dumps(response), content_type='application/json')


class ExtendedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(ExtendedTokenObtainPairSerializer, cls).get_token(user)
        token['first_name'] = user.first_name
        token['image'] = user.last_name
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = ExtendedTokenObtainPairSerializer
