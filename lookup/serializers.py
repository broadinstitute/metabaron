from .models import Lookup
from rest_framework import serializers


class LookupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lookup
        fields = ('short_id','description','url','method','paramtype','paramname' )
