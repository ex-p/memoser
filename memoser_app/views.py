import json
import logging

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from memoser_app.logic import verify_openapi_auth
from memoser_app.models import Mem, WhiteId
from memoser_app.serializers import MemSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RequestTokenView(View):
    def post(self, request):
        body = request.body.decode('utf-8')
        response = {'error': None, 'request': body}

        try:
            if not body:
                raise Exception('No data provided')
            data = json.loads(body)
            verified, mid = verify_openapi_auth(data['cookies'])
            if not verified:
                raise Exception('Not verified')
            if not WhiteId.objects.filter(mid=mid).exists():
                raise Exception('No access')
            name = 'vk{}'.format(mid)
            user = User.objects.filter(username=name)
            if not user.exists():
                name = data['user']['name'].split(' ')
                first_name = name[0]
                last_name = name[1]
                User.objects.create_user(username=name, first_name=first_name, last_name=last_name)
                user = User.objects.filter(username=name)
            user = user.first()
            refresh = ExtendedTokenObtainPairSerializer.get_token(user)
            response['refresh'] = str(refresh)
            response['access_token'] = str(refresh.access_token)
        except Exception as e:
            response['error'] = str(e)
        return HttpResponse(json.dumps(response), content_type='application/json')


class ExtendedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(ExtendedTokenObtainPairSerializer, cls).get_token(user)
        token['name'] = user.first_name
        token['image'] = user.last_name
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = ExtendedTokenObtainPairSerializer


class MemViewSet(viewsets.ModelViewSet):
    queryset = Mem.objects.all()
    serializer_class = MemSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), permissions.DjangoModelPermissions()]
