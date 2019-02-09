from rest_framework import serializers

from memoser_app.models import Mem


class MemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mem
        fields = ('title', 'description', 'image')
