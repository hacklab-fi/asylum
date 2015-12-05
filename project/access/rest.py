from rest_framework import viewsets, serializers
from .models import TokenType, Token, AccessType, Grant

class TokenTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TokenType

class TokenTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TokenTypeSerializer
    queryset = TokenType.objects.all()
    filter_fields = ('label',)

class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token

class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()
    filter_fields = ('label','owner', 'ttype', 'value','revoked')

class AccessTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccessType

class AccessTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AccessTypeSerializer
    queryset = AccessType.objects.all()
    filter_fields = ('label','bit','external_id')

class GrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grant

class GrantViewSet(viewsets.ModelViewSet):
    serializer_class = GrantSerializer
    queryset = Grant.objects.all()
    filter_fields = ('owner','atype')
